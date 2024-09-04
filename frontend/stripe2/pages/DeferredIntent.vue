<template>
  <v-card>
    <v-card-title>
      Yet Another Deferred Intent Payment Element Integration
    </v-card-title>
    <v-card-text>
      <v-form>
        <pre>TODO: Add form configure amount, mode, and currency</pre>
      </v-form>
      <div id="payment-element"></div>
    </v-card-text>
    <v-card-actions>
      <v-btn @click="mountElement">Mount</v-btn>
      <v-btn @click="submitElement">Submit</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  data: () => ({
    options: {
      amount: 1499,
      mode: 'payment',
      currency: 'usd'
    },
    elements: null,
    paymentElement: null
  }),
  methods: {
    async mountElement() {
      this.elements = await this.$stripe.elements(this.options)
      this.paymentElement = this.elements.create('payment')
      this.paymentElement.mount('#payment-element')
    },
    async submitElement() {

    }
  }
}
</script>

<style>

</style>
