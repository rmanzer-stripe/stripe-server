<template>
  <v-card>
    <v-card-title>Saved Payment Methods in the Payment Element</v-card-title>
    <v-card-text>
      Load the payment element with saved payment methods

      <div id="payment-element"></div>
    </v-card-text>
    <v-card-actions>
      <v-btn @click="getCustomerSession">Customer Sessions</v-btn>
      <v-btn @click="mountPE">Mount Element</v-btn>
      <v-btn>Submit Payment</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
data: () => ({
  element:null,
  elements:null,
  customerSession: null,
  intent: null,
  cust_id: 'cus_P0vjHXPRHV7mY9'
}),
  created() {
    this.getCustomerSession()
    this.createIntent()
  },
  methods: {
    async getCustomerSession() {

      const url = `/customers/${this.cust_id}/create_session/`
      const resp =  await this.$axios.$post(url)
      this.customerSession = resp
    },
    async createIntent(){
      const payload = {
        amount: 1099,
        currency: 'usd',
        customer: this.cust_id,
        payment_method_options: {
          card : {
            require_cvc_recollection: true
          }
        },
        payment_method_types: ['card']
      }
      const {intent} = await this.$axios.$post('/payment_intents/', payload)
      this.intent = intent
    },
    async mountPE() {
      if (this.customerSession === null) {
        alert("Customer Session needed")
        return;
      }
      this.elements = await this.$stripe.elements({
        mode: 'payment',
        currency: 'usd',
        amount: 1099,
        customerSessionClientSecret: this.customerSession.client_secret
      })
      this.element = this.elements.create('payment');
      this.element.mount('#payment-element')
      this.element.on('change', (ev) => {
        console.log(ev)
      })
    },
    async submitPayment() {
      this.intent = await this.createIntent()
      const {error} = await this.$stripe.confirmPayment({
        elements: this.elements,
        clientSecret: this.intent.client_secret,
        confirmParams: {
          return_url: this.$attrs.successUrl
        }
      })
      if (error) {
        console.error(error)
      }
    }
  }
}
</script>

<style>

</style>
