<template>
  <v-card>
    <v-card-title>Gimme Money! - Custom Flow</v-card-title>
    <v-card-subtitle>Please provide your payment method details in the form below. You will be charged {{ amount }} cents</v-card-subtitle>
    <v-card-text>
      <div id="payment_element"></div>
    </v-card-text>
    <v-card-actions class="py-6">
      <v-row justify="space-around">
        <v-btn class="deep-purple white--text" @click="createPaymentIntent">Create Intent</v-btn>
        <v-btn color="primary" @click="mountElement">
          Mount Element
        </v-btn>
        <v-btn class="teal darken-2 white--text" @click="submitPayment">Submit Payment</v-btn>
      </v-row>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  data: () => ({
     elements: null,
     payment_element: null,
     intent: null,
     amount: 1099,
     currency: 'usd',
     error: null,
     stripe: null,
  }),
  methods: {
    async createPaymentIntent() {
      const payload = {
        amount: this.amount,
        currency: this.currency,
        automatic_payment_methods: {
          enabled: true
        },
        account: this.$store.state.account.id
      }
      const { intent } = await this.$axios.$post('/payment_intents/', payload)
      console.log(intent)
      this.intent = intent
    },
    mountElement() {
      this.stripe = window.Stripe(this.$store.state.account.pk)
      this.elements = this.stripe.elements({clientSecret: this.intent.client_secret});
      this.payment_element = this.elements.create('payment', {fields: {
        billingDetails:{
          country: 'never'
        }
      }})
      this.payment_element.mount('#payment_element')
    },
    async submitPayment() {
      const {error}  = await this.stripe.confirmPayment({
        elements: this.elements,
        confirmParams: {
          return_url: `${window.location.origin}/success`
        }
      })
      if (error) {
        this.error = error
      }
    }
  }
}
</script>

