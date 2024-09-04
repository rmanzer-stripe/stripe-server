<template>
  <v-card class="my-8" :loading="loading" flat>
        <v-img
          class="white--text align-end"
          height="300px"
          src="https://images.pexels.com/photos/1034063/pexels-photo-1034063.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
          gradient="to top, rgba(0,0,0,0.5), rgba(0,0,0,0.2)"
          >
          <v-card-title>Deferred Intent Payments</v-card-title>
          <v-card-subtitle>Based on <a href="https://stripe.com/docs/payments/accept-a-payment-deferred">this doc</a></v-card-subtitle>
        </v-img>
        <v-card-text>

          <p class="text-h4">Provide Payment Details</p>
          <v-text-field v-if="options.mode == 'payment'" v-model="options.amount" type="number" label="Amount to Charge" class="mx-16 my-8"></v-text-field>
          <v-row class="ma-6 pa-6" justify="center">

            <v-tooltip top>
              <template v-slot:activator="{on, attrs}">
                <v-btn
                :disabled="payment_element==null"
                class="indigo white--text"
                @click="updateAmount"
                v-bind="attrs"
                v-on="on"
                >Update Amount</v-btn>
              </template>
              <span>Updates the amount <code>this.elements</code> is initialized with after Payment Element is mounted</span>
            </v-tooltip>
          </v-row>
          <customer-select  v-if="options.mode === 'setup' || options.mode=='subscription'" class="mx-16 my-8" @customer-selected="set_customer"/>
          <div v-if="error === null" id="payment-element-deferred"></div>
          <v-alert v-if="payment_element && selectedPaymentMethodType !== 'us_bank_account'" type="info" border="left" color="indigo" text>
            Non-Bank payment methods will be subjected to a 2.5% service fee
          </v-alert>
          <error-alert v-else :error="error" @dismissed="mountDeferred" />
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-row justify="space-around" class="my-5">
            <v-btn class="teal darken-3 white--text" @click="mountDeferred">Mount Element</v-btn>
            <v-radio-group v-model="options.mode" row :disabled="payment_element !== null">
              <v-radio label="Payment" value="payment"></v-radio>
              <v-radio label="Setup" value="setup"></v-radio>
              <v-radio label="Subscription" value="subscription"></v-radio>
            </v-radio-group>
            <v-btn class="deep-purple white--text" @click="createIntent">Create intent</v-btn>
            <v-btn class="indigo darken-3 white--text" :disabled="loading" @click="submit" >Submit</v-btn>
          </v-row>
        </v-card-actions>
      </v-card>
</template>

<script>
import CustomerSelect from '~/components/stripe/CustomerSelect.vue'
import ErrorAlert from '~/components/stripe/ErrorAlert.vue'
export default {
  components: { ErrorAlert, CustomerSelect },
 data: () => ({
    elements: null,
    payment_element: null,
    address_element: null,
    intent: null,
    customer: null,
    error: null,
    loading: false,
    selectedPaymentMethodType: null,
    options: {
      amount: 1099,
      mode: 'payment',
      currency: 'eur',
    }
 }),
 computed: {
    submitFunction() {
      if( this.options.mode === 'payment') return this.$stripe.confirmPayment
      if (this.options.mode === 'setup') return this.$stripe.confirmSetup
      return null
    },
    returnUrl () {
      return `${window.location.origin}/success`
    },
    paymentAmount() {
      if (this.selectedPaymentMethodType === 'us_bank_account') {
        return this.options.amount
      } else {
        return parseInt(this.options.amount * 1.025)
      }
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
    async confirmIntent(payload) {
      if (this.options.mode === 'setup') {
        const { error } = await this.$stripe.confirmSetup(payload)
        return error
      } else {
        const {error} = await this.$stripe.confirmPayment(payload)
        return error
      }
    },
    updateAmount() {
      const amount = Number(this.options.amount)
      console.log(amount);
      this.elements.update({amount})
    },
    mountDeferred() {
      // this.elements.update(this.options)
      const payOptions = {
        paymentMethodOrder: ['affirm'],
        layout: {
          type: 'accordion',
          defaultCollapsed: false,
          radios: true,
        }
      }
      this.payment_element = this.elements.create('payment', payOptions)
      this.payment_element.mount('#payment-element-deferred')
      this.payment_element.on('change',(event) => {
        this.setPaymentMethodType(event)
      })
    },
    async submit() {
      this.loading = true
      const {error: submitError} = await this.elements.submit()
      if (submitError) {
        this.error = submitError
        this.loading = false
        return;
      }
      // Ths takes long enough that Apple Pay won't go through if I include it!
      // const {error, confirmationToken} = await this.$stripe.createConfirmationToken({
      //       elements: this.elements,
      //       params: {
      //         payment_method_data: {
      //           billing_details: {
      //             name: 'Jenny Rosen',
      //             address: {
      //               country: 'US',
      //               postal_code: '90210',
      //               state: 'CA',
      //               city: 'Beverly Hills',
      //               line1: '123 Townsend St',
      //               line2: '',
      //             }
      //           }
      //         }
      //       }
      //     });
      // if (error) {
      //   this.error = error
      //   this.loading = false
      //   return;
      // } else {
      //   console.log(confirmationToken);
      // }

      const success = await this.createIntent()
      if (success) {
        const confirmPayload = {
          elements: this.elements,
          clientSecret: this.intent.client_secret,
          confirmParams: {
            return_url: this.returnUrl
          }
        }
        console.log(confirmPayload);
        const error = await this.confirmIntent(confirmPayload)
        if (error) {
          console.log(error)
          this.error = error
        }
      }
      this.loading = false
    },
    async createIntent() {
      if (this.options.mode === 'payment') {
        console.log('Creating Payment Intent');
        const payload = {
          amount: this.paymentAmount,
          currency: this.options.currency,
          automatic_payment_methods: {
            enabled: true
          }
        }
        if (this.selectedPaymentMethodType === 'card') {
          payload.setup_future_usage = "off_session"
        }
        const {intent} = await this.$axios.$post('payment_intents/', payload)
        console.log(intent);
        this.intent = intent
        return true
      } else if (this.customer == null) {
          this.error = {code: 'missing_customer', type: 'invalid_request_error', message: "Please set a customer before creating a Setup Intent"}
          return false
        } else {
          console.log('Creating setup intent');
          const {intent } = await this.$axios.$post('setup_intents/', {
            customer: this.customer.id,
            automatic_payment_methods: {
              enabled: true
            }
          })
          this.intent = intent
          return true
        }
    },
    setPaymentMethodType(ev) {
      this.selectedPaymentMethodType = ev.value.type
      if (ev.value.type === 'card') {
        console.log('Updating element to save PM');
        this.elements.update({setupFutureUsage: 'off_session'})
      }
    }
  },
}
</script>
