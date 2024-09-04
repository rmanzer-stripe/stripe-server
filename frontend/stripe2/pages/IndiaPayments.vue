<template>
  <v-container class="">
    <v-row v-show="error !== null">
      <error-alert :error="error" />
    </v-row>
    <v-row justify="center">
      <v-col>
        <v-card>
          <v-toolbar flat>
            <v-toolbar-title>India Payments</v-toolbar-title>
            <v-spacer></v-spacer>

                <v-btn dark color="indigo" @click="show_object = !show_object">
                  Stripe Object
                </v-btn>
          </v-toolbar>
          <v-card-text>
            <div id="payment-element">
              Do things, also stuff
            </div>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-row justify="space-around" class="my-6">
              <v-btn dark color="light-blue" @click="get_prices">Get Price</v-btn>
              <v-btn dark color="amber darken-4" @click="create_clock">Test Clock</v-btn>
              <v-btn dark color="green" @click="create_customer">Customer</v-btn>
              <v-btn dark color="purple" @click="create_subscription">Subscription</v-btn>
              <v-btn dark color="teal darken-1" @click="mount_element">Mount PE</v-btn>
            </v-row>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col v-show="show_object">
        <stripe-object-view :stripe-object="stripeObject" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ErrorAlert from '~/components/stripe/ErrorAlert.vue'
import StripeObjectView from '~/components/stripe/StripeObjectView.vue'
export default {
  components: { StripeObjectView, ErrorAlert },
  data: () => ({
    clock: null,
    customer: null,
    price: null,
    subscription: null,
    currency: 'inr',
    error: null,
    show_object: false,
    elements: null,
    element: null,
  }),
  computed: {
    stripeObject() {
      if (this.subscription !== null) {
        return this.subscription
      }
      else if (this.customer) {
        return this.customer
      } else if (this.price){
        return this.price
      }
      else {
        return {}
      }
    }
  },
  methods: {
    async create_clock(){
      const now = ~~(Date.now() /1000)
      const payload = {
        frozen_time: now,
        name: 'India Test Clock'
      }
      const url = '/test_clocks/'
      const {test_clock} = await this.$axios.$post(url, payload)
      this.clock = test_clock
    },
    async create_customer() {
      const payload = {
        name: 'Test India',
        email: 'test@india.co',
      }
      if( this.clock !== null) {
        payload.test_clock = this.clock.id
      }
      const {customer} = await this.$axios.$post('/customers/', payload)
      if (customer) {
        this.customer = customer
      }
    },
    async get_prices(){
      const url = `/prices/filter_currency/?currency=${this.currency}`
      const prices = await this.$axios.$get(url)
      if (prices.length > 0) {
        const price = prices[0]
        if (price) {
          this.price = price.data
        }
      }
    },
    async create_subscription() {
      if (this.customer != null && this.price !== null) {
        const payload = {
          customer: this.customer.id,
          payment_behavior: "default_incomplete",
          payment_settings: {
            save_default_payment_method: "on_subscription"
          },
          items: [
            {
              price: this.price.id
            }
          ],
          metadata: {
            reason: "India recurring payments walkthrough"
          },
          expand: ['latest_invoice.payment_intent']
        }
        this.subscription = await this.$axios.$post('/subscriptions/', payload)
      } else {
        this.error = {code: 'missing_parameters', message: "Please provide a Customer and Price before generating a Subscription"}
      }
    },
    mount_element() {
      const client_secret = this.subscription.latest_invoice.payment_intent.client_secret
      this.elements = this.$stripe.elements({clientSecret: client_secret})
      this.element = this.elements.create('payment')
      this.element.mount('#payment-element')
    },
    async confirm_payment() {
      const options = {
        elements: this.elements,
        confirmParams: {
          return_url: `${window.location.origin}/success`,
        },
        redirect: 'if_required'
      }
      const {error} = await this.$stripe.confirmPayment(options)
      if (error) {
        this.error = error
      }
    },
    async advance_clock() {

    }
  }
}
</script>


