<template>
  <v-row align="center" justify="center">
    <v-form>
      <stripe-element-payment
        ref="paymentElementRef"
        :elements-options="elementsOptions"
        :confirm-params="confirmParams"
        />
    <v-btn @click="payNow">
      <v-icon>mdi-dollar</v-icon>
      Pay
    </v-btn>
    </v-form>
  </v-row>

</template>

<script>
import { StripeElementPayment } from '@vue-stripe/vue-stripe';
export default {
  components: {
    StripeElementPayment
  },
  props: {
    elementsOptions: {type: Object, required: false, default: () => ({appearance: {}}) },
    confirmParams: {type: Object, required: false, default: () =>({return_url: "https://example.com"})},
  },

}
</script>

