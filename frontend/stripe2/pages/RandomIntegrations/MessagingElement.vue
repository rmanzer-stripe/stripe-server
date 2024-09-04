<template>
<v-card :loading="loading">
  <v-card-title>
    Payment Messaging Element
  </v-card-title>
  <v-card-text>
    <div id="message-element"></div>
  </v-card-text>

  <v-card-actions>
    <v-btn @click="mountElement">Mount</v-btn>
  </v-card-actions>
</v-card>

</template>

<script>
export default {
  data: () => ({
    elements: null,
    element: null,
    loading: false

  }),
  created() {

  },
  methods: {
    mountElement() {
      this.loading = true
      const options =  {
      amount: 55000, // $550.00 USD
      currency: 'USD',
      paymentMethodTypes: ['afterpay_clearpay'],
      // the country that the end-buyer is in
      countryCode: 'US',
    }
      this.elements = this.$stripe.elements()
      this.element = this.elements.create('paymentMethodMessaging', options)
      this.element.mount('#message-element')
      this.element.on('ready', (ev) => {
        this.loading = false
      })
    }
  }
}
</script>

<style>

</style>
