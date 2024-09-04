<template>
<v-card flat>
  <v-card-title>Client Side Submit & Process</v-card-title>
  <v-card-text>
    <div id="order-payment-element">
      <v-progress-circular indeterminate color="teal" size="100"/>
    </div>
    <v-alert v-if="error !== null" type="error" text v-text="error.message"></v-alert>
  </v-card-text>
  <v-card-actions class="d-flex justify-center align-center">
    <v-btn ref="payBtn" type="submit" color="teal darken-1 white--text" :disabled="disabled" @click="submitAndConfirm" >
      <v-icon>mdi-currency-usd</v-icon>
      Pay
    </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import {loadStripe} from '@stripe/stripe-js';

export default {
  props: {
    clientSecret: {type: String, required: true}
  },
  data: () => ({
    stripe: null,
    elements: null,
    paymentElement: null,
    error: null,
    disabled: false,
  }),
  async created() {
    this.stripe = await loadStripe('pk_test_51JticYIlCeH6bP8REulC9GlUO09hWuGsCljwJ3VNWhqqLmTTW0CedWXOoABWyXkplmqMtwfA4SiXkdeqCMvesIii00BCpJb9Vb', {
      betas: ['process_order_beta_1'],
      apiVersion: "2020-08-27; orders_beta=v4"
    })
    this.elements = this.stripe.elements({clientSecret: this.clientSecret})
    this.paymentElement = this.elements.create('payment')
    this.paymentElement.mount('#order-payment-element')
  },
  methods: {
    async submitAndConfirm() {
      this.disabled = true
      const {error} = await this.stripe.processOrder({
        elements: this.elements,
        confirmParams: {
          return_url: 'http://localhost:3100/orders/success'
        }
      })
      if (error) {
        this.error = error
      }
    }
  }
}
</script>

