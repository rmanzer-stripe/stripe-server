<template>
  <v-card class="ma-4">
    <v-row>
      <v-col v-if="clientSecret === null" align-self="center" align="center" justify="center">
        <v-btn class="primary" @click="createPaymentIntent">Generate Payment Intent</v-btn>

      </v-col>
      <v-col v-else cols="12" md="8" offset-md="2" align="center" justify="center">
        <v-alert type="success" border="left" outlined>Payment Intent Created</v-alert>
      </v-col>
    </v-row>
    <v-row>
      <v-container class="mx-10">
        <!-- <p class="text-h5">Link Info</p>
        <v-row class="mt-4 pa-6">
          <v-col cols="12" md="6">
          <div v-show="clientSecret !== null" id="link-authentication-element"></div>
          <v-alert v-show="clientSecret === null" type="info" border="left" outlined>
            Link Authentication Element will be loaded here once Payment Intent is generated
          </v-alert>
        </v-col>
        <v-col cols="12" md="6">
          <div v-show="clientSecret !== null" id="link-address-element"></div>
          <v-alert v-show="clientSecret === null" type="info" outlined border="left">
            Shipping Address element will be loaded once Payment Intent is generated
          </v-alert>
        </v-col>
        </v-row>
        <p class="text-h5 mb-4">Payment Info</p>
        <v-row class="my-4 pa-6" justify="center" align-items="center">

        <div v-show="clientSecret !== null" id="payment-element"></div>
        <v-alert v-show="clientSecret === null" type="info" border="left">
            Payment Element will be loaded here once Payment Intent is generated
          </v-alert>
        </v-row>

        <v-row class="mt-8" align="center" justify="center">
          <v-col justify="center" align="center">
            <v-btn class="primary" @click="submitPayment">Submit</v-btn>
          </v-col>
        </v-row> -->
        <form id="payment-form" @submit="submitPayment">
          <h3>Contact info</h3>
          <div id="link-authentication-element"></div>
          <div id="link-address-element"></div>

          <h3>Payment</h3>
          <div id="payment-element"></div>
          <v-row justify="center" class="my-5">
            <v-btn type="submit" class="deep-purple white--text">Submit</v-btn>
          </v-row>

        </form>
      </v-container>
    </v-row>
    <v-row>
      <v-col v-if="error !== null" cols="12" md="8" offset-md="2" >
        <v-alert type="error" border="left" >{{ error.message }}</v-alert>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import {loadStripe} from '@stripe/stripe-js';

export default {
data: () => ({
  url: 'payment_intents/',
  params: {
    currency: 'USD',
    amount: 1999,
    payment_method_types: [
      'link',
      'card'
    ],
  },
  clientSecret: null,
  stripe: null,
  elements: null,
  appearance: {},
  loader: 'auto',
  error: null,
}),
created() {
  this.loadStripeElements()
},
methods: {
  async loadStripeElements() {
    this.stripe = await loadStripe('pk_test_51JticYIlCeH6bP8REulC9GlUO09hWuGsCljwJ3VNWhqqLmTTW0CedWXOoABWyXkplmqMtwfA4SiXkdeqCMvesIii00BCpJb9Vb', {
      apiVersion: "2020-08-27"
    })
  },
  async createPaymentIntent() {
    const {intent}  = await this.$axios.$post(this.url, this.params)
    this.clientSecret = intent.client_secret
    console.log("Intent received, secret set", this.clientSecret)
    this.loadMountElements()
  },
  loadMountElements() {
    if (this.clientSecret !== null) {
      this.elements = this.stripe.elements({clientSecret: this.clientSecret, appearance: this.appearance, loader: this.loader})
      console.log("Elements initialized");
    }
    const linkAuthElement = this.elements.create('linkAuthentication');
    const addressElement = this.elements.create('address', {mode: 'shipping'})
    const paymentElement = this.elements.create('payment', {
      fields: {
        address: 'never'
      }
    })
    linkAuthElement.mount('#link-authentication-element')
    addressElement.mount('#link-address-element')
    paymentElement.mount('#payment-element')
  },
  async submitPayment() {
    const {error} = await this.stripe.confirmPayment({
      elements: this.elements,
      confirmParams: {
        return_url: "https://example.com/"
      }
    })
    if (error) {
      this.error = error
    }
  }
},

}
</script>
