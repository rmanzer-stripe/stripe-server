<template>
  <div id="confirm-screen">
    <v-row align-content="center">
      <p class="text-h4">{{ agreement }}</p>
      <v-card flat>
        <v-card-title>Payment Method Details</v-card-title>
        <v-card-text>
          <v-row justify="space-around">

          </v-row>
        </v-card-text>
      </v-card>
    </v-row>
  </div>
</template>

<script>
export default {
  props: {
    confirmationToken: {type: Object, required: false, default: () => {}},
    mode: {type: String, required: false, default: 'payment'},
    amount: {type: Number, required: false, default: 1099},
    currency: {type: String, required: false, default: 'usd'}
  },
  data: () => ({
    pmType: null
  }),
  computed: {
    agreement() {
      let agreeStr = ""
      switch (this.mode) {
        case 'payment':
          agreeStr= `You agree to use the Payment Method details below to pay me ${this.amount} ${this.currency}`
          break;
        case 'setup':
          agreeStr = `You agree to save the Payment Method details below for future use`
          break;
        case 'subscription':
          agreeStr = `You agree to use the Payment Method details below for recurring payments`
      }
      return agreeStr
    },
    paymentMethod() {
      const pmPreview = this.confirmationToken.payment_method_preview;
      if (pmPreview.type === 'card') {
        return pmPreview.card
      } else {
        return pmPreview.us_bank_account
      }
    },

  },
}
</script>

<style>

</style>
