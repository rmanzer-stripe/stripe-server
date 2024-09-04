<template>
  <v-row justify="space-around">
    <v-col cols="12" sm="6">
      <v-btn>Create PI</v-btn>
    </v-col>
    <v-col cols="12" sm="6">
      <div id="paymentRequestButton"></div>
    </v-col>
  </v-row>
</template>

<script>
export default {
  data: () => ({
    paymentRequestData: {
      country: 'US',
      currency: 'usd',
      total: {
        label: 'Demo total',
        amount: 1099
      },
      requestPayerName: true,
      requestPayerEmail: true,
      requestShipping: true,
      shippingOptions: [
        {
          id: "ground",
          label: "Ground Shipping",
          detail: "3 day ground shipping via UPS",
          amount: 1095,
        },
        {
          id: "air",
          label: "Air Shipping",
          detail: "Next day ground shipping via DHL",
          amount: 2595,
        },
      ],
    },
    elements: null,
    paymentRequest: null,
    PRB: null
  }),
  methods: {
    async createPI() {
      const payload = {
        amount: 1099,
        currency: 'usd'
      }
      const {clientSecret, id, error} = await this.$axios.$post('/payment_intents/', payload);
      if (error) {
        console.error(error);
      }
      return {clientSecret, id}
    },
    instantiate() {
      this.elements = this.$stripe.elements()
      this.paymentRequest = this.$stripe.paymentRequest(this.paymentRequestData);
      this.PRB = this.elements.create('paymentRequestButton', {paymenRequest: this.paymentRequest})
    },
    async validateMount() {
      const result = await this.paymentRequest.canMakePayment()
      console.log(result);
      if (result) {
        this.PRB.mount('#paymentRequestButton')
      } else {
        console.log('No Wallet available');
      }
    }
  },
  created() {
    this.instantiate()
  },
  mounted() {
    this.validateMount()
  }
}
</script>
