<template>
  <v-card>
    <v-card-text>
      <v-row>
        <div id="payment-element"></div>

      </v-row>
    </v-card-text>
    <v-divider></v-divider>
    <v-card-actions class="my-4">
      <v-row justify="space-around">
        <v-btn @click="submitPayment">Submit</v-btn>
      </v-row>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
 data: () => ({
  elements: null,
  payment_element: null,
  payment_intent: null,
  error: null,
  intentOptions: {
    amount: 2099,
    currency: 'usd',
    automatic_payment_methods: {enabled: true}
  },
  confirmParams: {
    return_url: `${window.location.origin}/success`
  }
 }),
 methods: {
  buildPayload() {
    return this.intentOptions
  },
  async createPaymentIntent() {
    const payload = this.buildPayload()
    const {intent, error} = await this.$axios.$post('/payment_intents/', payload)
    if (error) {
      this.error = error
    } else {
      this.payment_intent = intent
    }
  },
  mountElement() {
    if (this.payment_intent) {
      this.elements = this.$stripe.elements(
        {clientSecret: this.payment_intent.client_secret}
      )
    } else {
      this.elements = this.$stripe.elements({
        mode: 'payment',
        currency: this.intentOptions.currency,
        amount: this.intentOptions.amount
      })
    }
    this.payment_element = this.elements.create('payment')
    this.payment_element.mount('#payment-element')
  
  },
  async submitPayment() {
    const {error} = await this.$stripe.confirmPayment({
      elements: this.elements,
      confirmParams: this.confirmParams
    })
    if (error) {
      this.error = error
    }
  }
 }
}
</script>
