<template>
  <v-card>
    <v-card-title>Payment Request Button</v-card-title>
    <v-card-text>
      <div id="prb"></div>
      <object-viewer :object="myObject" class="my-5"></object-viewer>
    </v-card-text>
    <v-card-actions>
      <v-row justify="space-around" class="my-4">
        <v-btn @click="canMP" class="amber darken-2 white--text">Payment Options</v-btn>
        <v-btn class="teal darken-2 white--text" @click="mountPRB">Mount Button</v-btn>
        <v-btn class="indigo darken-2 white--text" @click="getIntent">Get Intent</v-btn>
      </v-row>
    </v-card-actions>
  </v-card>
</template>

<script>
import objectViewer from '~/components/core/objectViewer.vue'
export default {
  components: { objectViewer },
  data: () => ({
    elements: null,
    element: null,
    intent: null,
    request: null,
    myObject: {},
    displayItems: [1,2,3]
  }),
  created() {
    this.createRequest()
  },
  methods: {
    createRequest() {
      const payload = {
        country: 'US',
        currency: 'usd',
        total: {
          label: 'Demo total',
          amount: 1099
        },
        requestPayerName: true,
        requestPayerEmail: true,
        requestShipping: true,
      }
      this.request = this.$stripe.paymentRequest(payload)
      this.elements = this.$stripe.elements()
      this.element = this.elements.create('paymentRequestButton', {
        paymentRequest: this.request
      })
      this.myObject = this.request

      this.request.on('paymentmethod', async(ev) => {
       await this.confirmIntent(ev)
      })
      this.request.on('shippingoptionchange', ({shippingOption, updateWith}) => {
        const subtotalAmount = 1099

        updateWith({
          status: 'success',
          total: {
            amount: 1099 + shippingOption.amount,
            label: 'Total'
          },
          displayItems: [
            ...([1,2,3].length ? this.displayItems : [{label: 'Subtotal', amount: subtotalAmount}]),
            {
              label: 'Shipping',
              amount: shippingOption.amount
            }
          ]
        })
      })
    },
    async canMP() {
      const result = await this.request.canMakePayment()
      if (result !== null) {
        this.myObject = result
      } else {
        this.myObject = {outcome: result}
      }

    },
    mountPRB() {
      this.element.mount('#prb')
    },
    async getIntent() {
      const {intent} = await this.$axios.$post('/payment_intents/', {
        amount: 1099,
        currency: 'usd',
      })
      this.intent = intent
      this.myObject = intent
    },
    async confirmIntent(ev) {
      if (this.intent === null) {
            alert('No Payment Intent! No confirm for you!')
        return
      }
      const {paymentIntent, error: confirmError} = await this.$stripe.confirmCardPayment(this.intent.client_secret, {
        payment_method: ev.paymentMethod.id,
      }, {handleActions: false})
      if (confirmError) {
        this.myObject = confirmError
      } else {
        this.myObject = paymentIntent
      }
    }
  }
}
</script>

<style>

</style>
