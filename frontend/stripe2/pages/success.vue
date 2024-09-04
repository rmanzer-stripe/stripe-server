<template>
  <v-row justify="center" class="my-8">
    <v-card>
      <v-img
        src="https://images.pexels.com/photos/684385/pexels-photo-684385.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
        height="600px"
        gradient="to top, rgba(0,0,0,0.6), rgba(0,0,0,0.01)"
        class="align-end white--text"
      >
        <v-card-title class="text-h4">Success!</v-card-title>
        <v-divider color="white"></v-divider>
        <v-card-subtitle class="text-h6">You did the thing, whatever that was!</v-card-subtitle>
    </v-img>
    <v-card-text>
      This is where I put stuff about the thing you did, if I want
      <object-viewer :object="stripeObject" />
    </v-card-text>
    <v-divider></v-divider>
    <v-card-actions class="justify-center my-3">
      <span class="mx-8">Buttons are neat</span>
      <v-btn outlined color="blue-grey" @click="setStripeObject">Refresh Object</v-btn>
      <v-btn color="teal" class="white--text" @click="GoHome">Go Home</v-btn>
    </v-card-actions>
    </v-card>
  </v-row>
</template>

<script>
import objectViewer from '~/components/core/objectViewer.vue'
export default {
  components: { objectViewer },
  name: 'SuccessPage',
  data: () => ({
    stripeObject: null,
    stripe: null,

  }),
  mounted() {
    this.setStripeObject()
  },
  methods: {
    searchParams(param) {
      if ( window.location.search.includes(param) ) {
        const params = new URLSearchParams(window.location.search)
        return params.get(param)
      } else {
        return false
      }
    },
    async getPaymentIntent(param) {
        const {paymentIntent} = await this.stripe.retrievePaymentIntent(param)
        return paymentIntent
    },
    async fetchPaymentIntent(param) {
      const url = `/payment_intents/${param}/`
      const {intent} = await this.$axios.$get(url, {account: this.$store.state.account.id})
      return intent
    },
    async getSetupIntent(param){
        const {setupIntent} = await this.stripe.retrieveSetupIntent(param)
        return setupIntent
    },
    async getCheckoutSession(param) {
      const {session} = await this.$axios.$get(`/checkout_sessions/${param}/`, {account: this.$store.state.account.id})
      return session
    },
    async getStripeObject(){
      this.stripe = window.Stripe(this.$store.state.account.pk)
      const piId = this.searchParams('payment_intent')
      const piSec = this.searchParams('payment_intent_client_secret')
      const siId = this.searchParams('setup_intent')
      const chId = this.searchParams('session_id')
      if (piSec) {
        return await this.getPaymentIntent(piSec)
      } else if (piId){
        return await this.fetchPaymentIntent(piId)
      } else if (siId) {
        return await this.getSetupIntent(siId)
      } else if (chId) {
        return await this.getCheckoutSession(chId)
      } else {
        return {}
      }
    },
  async setStripeObject() {
    this.stripeObject = await this.getStripeObject()
  },
    GoHome() {
      this.$router.push({name: 'index'})
    }
  },
}
</script>

