<template>
  <v-row>
    <v-col cols="12" sm="10" offset-sm="1">
      <v-card>
        <v-toolbar
          color="indigo"
          dark
          flat
        >
        <v-toolbar-title>Deferred & Multi-Step Payment Confirmation/Processing</v-toolbar-title>
        <v-spacer></v-spacer>
        <template v-slot:extension>
          <v-tabs
          v-model="tab"
          align-with-title>
            <v-tabs-slider color="white"></v-tabs-slider>

            <v-tab
              v-for="item in tab_items"
              :key="item.name"
             >
             {{ item.name }}
            </v-tab>
          </v-tabs>
        </template>
      </v-toolbar>
      <v-card-text>
          <v-tabs-items v-model="tab">
            <v-tab-item
              v-for="item in tab_items"
              :key="item.name"
            >
             <component :is="item.component" />
            </v-tab-item>
          </v-tabs-items>
        </v-card-text>
      </v-card>
      <!-- Deferred Intent Card -->
      <!-- <deferred-intent-card /> -->
      <!-- Two Step Confirmation Card -->
      <!-- <two-step-confirm-card /> -->
      <!-- Server Finalized Cards-->
     <!-- <finalize-on-server /> -->
    </v-col>
  </v-row>
</template>

<script>
import DeferredIntentCard from '~/components/stripe/multiStep/DeferredIntentCard.vue'
import TwoStepConfirmCard from '~/components/stripe/multiStep/TwoStepConfirmCard.vue'
import FinalizeOnServer from '~/components/stripe/multiStep/FinalizeOnServer.vue'

export default {
  components: { DeferredIntentCard, TwoStepConfirmCard, FinalizeOnServer },

  // eslint-disable-next-line vue/order-in-components
  name: 'MultiStep',
  data: () => ({
    elements: null,
    PaymentElementDeferred: null,
    AddressElement: null,
    options: {
      mode: 'payment',
      amount: 1099,
      currency: 'usd',
      appearance:{}
    },
    intent: null,
    customer: null,
    error: null,
    loading: false,
    tab: null,
    tab_items: [
      {
        name: "Deferred Intent",
        component: "DeferredIntentCard"
      },
      {
        name: "2 Step Confirmation",
        component: "TwoStepConfirmCard"
      },
      {
        name: "Finalize On Server",
        component: "FinalizeOnServer"
      }
    ]
  }),
  head: {
    title: 'Multi Step Checkout Flows'
  },
  computed: {
    submitFunction() {
      if( this.options.mode === 'payment') return this.$stripe.confirmPayment
      if (this.options.mode === 'setup') return this.$stripe.confirmSetup
      return null
    },
    returnUrl () {
      return `${window.location.origin}/success`
    }
  },
  created() {
    this.elements = this.$stripe.elements(this.options)
  },
  methods: {
    set_customer(e) {
      console.log("Setting customer: ", e)
      this.customer = e
    },
    mountDeferred() {
      let options = this.options
      if (this.options.mode === 'setup') {
        options = {mode: this.options.mode, appearance: this.options.appearance}
      }
      this.elements.update(options)
      this.PaymentElementDeferred = this.elements.create('payment')
      this.PaymentElementDeferred.mount('#payment-element-deferred')
    },
    async submitDeferred() {
      this.loading = true
      const {error: submitError} = await this.elements.submit()
      if (submitError) {
        this.error = submitError
        this.loading = false
        return;
      }
      const success = await this.createIntent()
      if (success) {
        const {error} = await this.submitFunction({
          elements: this.elements,
          clientSecret: this.intent.client_secret,
          confirmParams: {
            return_url: this.returnUrl
          }
        })
        if (error) {
          this.error = error
        }
      }
      this.loading = false
    },
    async createIntent() {
      if (this.options.mode === 'payment') {
        this.intent = await this.$axios.$post('payment_intents/', {
          amount: this.options.amount,
          currency: this.options.currency,
          automatic_payment_methods: {
            enabled: true
          }
        })
        return true
      } else if (this.customer == null) {
          this.error = {code: 'missing_customer', type: 'invalid_request_error', message: "Please set a customer before creating a Setup Intent"}
          return false
        } else {
          this.intent = await this.$axios.$post('setup_intents/', {
            customer: this.customer.id,
            automatic_payment_methods: {
              enabled: true
            }
          })
          return true
        }
    }
  },
}
</script>
