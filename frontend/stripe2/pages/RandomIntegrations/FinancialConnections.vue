<template>
  <v-card>
    <v-card-title>Financial Connections</v-card-title>
    <v-card-subtitle>This flow will create a simple Payment Intent that only accepts <code>us_bank_account</code> payment methods and confirm it using the Payment Element</v-card-subtitle>
    <v-card-text>
      <div id="payment-form"></div>
    </v-card-text>
    <v-card-actions class="jusity-around">
      <v-btn color="teal" @click="loadElements">Load</v-btn>
      <v-btn color="primary" @click="confirmIntent">Submit</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  data: () => ({
    elements: null,
    element: null,
    customer: 'cus_PWgzHzIEp7xYLC',
    intent: null,
  }),
  created() {
    this.createPaymentIntent()
  },
  methods: {
    async createPaymentIntent() {
      const payload = {
        amount: 20099,
        currency: 'usd',
        customer: this.customer,
        payment_method_types: ['us_bank_account'],
        payment_method_options: {
          us_bank_account: {
            financial_connections: {
              permissions: ['transactions', 'payment_method']
            }
          }
        }
      }
      const {intent} = await this.$axios.$post('/payment_intents/', payload)
      this.intent = intent
    },
    loadElements() {
      if (this.intent !== null) {
        this.elements = this.$stripe.elements({clientSecret: this.intent.client_secret})
        this.element  = this.elements.create('payment')
        this.element.mount('#payment-form')
      }
    },
      async confirmIntent() {
        const {error} = await this.$stripe.confirmPayment({
          elements: this.elements,
          confirmParams: {
            return_url: 'https://rmanzer-app.tunnel.stripe.me/success'
          }
        })
        if (error) {
          console.log(error);
        }
      }
    }
  }

</script>

<style>

</style>
