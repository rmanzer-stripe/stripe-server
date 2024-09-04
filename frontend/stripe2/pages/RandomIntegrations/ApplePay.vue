<template>
  <div>
    <p class="text-h3">Apple Pay with Merchant Tokens</p>
    <v-row justify="center">

      <v-col cols="12" lg="4" md="6" sm="10">
        <v-form>
          <v-select v-model="mpan_type" :items="mpan_types" label="MPAN Type"></v-select>
          <div id="ece" class="my-6 teal lighten-4">
            Placeholder Content. ECE goes here
          </div>
        </v-form>
      </v-col>
      <v-col cols="12" lg="1" md="1" sm="2" class="mx-5">
        <v-tooltip right>

          <template v-slot:activator="{on, attrs}">
            <v-btn :disabled="mpan_type === null" @click="mountElement" v-bind="attrs" v-on="on">Mount Element</v-btn>

          </template>
          <span v-if="mpan_type === null">Select an MPAN type first</span>
        </v-tooltip>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  data: () => ({
    mpan_payloads: {
      recurringPaymentRequest: {
        paymentDescription: 'My subscription',
        managementURL: 'https://example.com/billing',
        regularBilling: {
          amount: 2500,
          label: 'Monthly subscription fee',
          recurringPaymentIntervalUnit: 'month',
          recurringPaymentIntervalCount: 1,
        },
      },
      automaticReloadPaymentRequest: {
        paymentDescription: 'My subscription',
        managementURL: 'https://example.com/billing',
        regularBilling: {
          amount: 2500,
          label: 'Automatic Reload',
          automaticReloadPaymentThresholdAmount: 500
        },
      },
      deferredPaymentRequest: {
        paymentDescription: 'My deferred payment',
        managementURL: 'https://example.com/billing',
        deferredBilling: {
          amount: 2500,
          label: 'Deferred Fee',
          deferredPaymentDate: new Date('2024-06-01')
        },
      },
    },
    mpan_type: null,
    elements: null,
    element: null,
    error: null,
    client_secret: null
  }),
  computed: {
    mpan_types() {
      return Object.keys(this.mpan_payloads)
    },
    currentDate() {
      return new Date();
    }
  },
  methods: {
    async createPaymentIntent() {
      const { intent } = await this.$axios("/payment_intents", {
        amount: 2500,
        currency: 'usd'
      })
      this.client_secret = intent.client_secret
    },
    mountElement() {
      this.elements = this.$stripe.elements({
          mode: 'payment',
          amount: 2500,
          currency: 'usd',
        })
        this.element = this.elements.create('expressCheckout')
        this.element.mount('#ece')
        this.element.on('click', (event) => {
          this.onClick(event)
        });
        this.element.on('confirm', () => {
          this.confirmPayment()
        })
    },
    onClick(event) {
      const type = this.mpan_type
      const payload = this.mpan_payloads[type]
      const mpan_payload = {
        type: payload
      }
      event.resolve({
        applePay: mpan_payload
      })
    },
    async confirmPayment(event) {
      const {error: SubmitError} = await this.elements.submit();
      if (SubmitError) {
        this.error = SubmitError
        return
      }
      if (this.client_secret === null) {
        const success = await this.createPaymentIntent()
        if (!success) {
          return
        }
      }
      const {error} = await this.$stripe.confirmPayment({
        elements: this.elements,
        clientSecret: this.client_secret,
        confirmParams: {
          return_url: `${window.location.origin}/success`
        }
      })
      if (error) {
        this.error = error
      }
      console.log("stuff");
    }
  }
}
</script>


