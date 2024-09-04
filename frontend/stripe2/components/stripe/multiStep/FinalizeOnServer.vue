<template>
   <v-card class="my-8" flat>
        <v-img
          class="white--text align-end"
          height="300px"
          src="https://images.pexels.com/photos/2881233/pexels-photo-2881233.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
          gradient="to top, rgba(0,0,0,0.5), rgba(0,0,0,0.2)"
          >
          <v-card-title>Server-Finalized Payments</v-card-title>
          <v-card-subtitle>Based on <a href="https://stripe.com/docs/payments/finalize-payments-on-the-server">this doc</a></v-card-subtitle>
        </v-img>
        <v-card-text>
          <v-alert v-if="success" border="left" colored-border color="green" type="success" outlined>
            <p class="text-h4">Success!</p>
            <v-divider></v-divider>
            <p>Payment confirmed! Woohoo 🎉</p>
          </v-alert>
          <v-row>
            <v-col cols="12" sm="12">
              <v-form class="my-8" :disabled="success">
                <p class="text-h4">Payment Intent / Address Information </p>
                <v-row>
                  <v-col cols="12" sm="3" class="ma-2">
                    <v-text-field type="number" v-model="options.amount" label="Amount to charge"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="3" class="ma-2">
                    <currency-select :default="this.options.currency" @currency="setCurrency"/>
                  </v-col>
                  <v-col cols="12" sm="3" class="ma-2">
                    <v-select v-model="addressOptions.mode" :items="addressModes" label="Address Mode"></v-select>
                  </v-col>
                </v-row>
                <v-row justify="center">
                  <p class="text-h4"> {{ addressOptions.mode  }} Address</p>
                  <v-col cols="12" sm="12">
                    <div id="address-element"></div>
                  </v-col>
                </v-row>
              </v-form>
            </v-col>
            <v-col v-if="error !== null">
              <error-alert :error="error" />
            </v-col>
          </v-row>

          <div id="payment-element-finalize"></div>
        </v-card-text>
        <v-card-actions class="my-5">
          <v-row justify="space-around" class="py-6">
            <v-btn color="green darken-4 white--text" @click="mountElement" :disabled="success">Mount</v-btn>
            <v-switch v-model="useConfirmationToken" :label="`Use Confirmation Token - ${useConfirmationToken}`"></v-switch>
            <v-btn color="primary" @click="submitPayment" :disabled="success">Submit</v-btn>
          </v-row>
        </v-card-actions>
      </v-card>
</template>

<script>
import CurrencySelect from '../CurrencySelect.vue'
import ErrorAlert from '../ErrorAlert.vue'
export default {
  components: { CurrencySelect, ErrorAlert },

  data: () => ({
    elements: null,
    paymentElement: null,
    addressElement: null,
    addressOptions: {
      mode: 'shipping'
    },
    addressModes:['billing', 'shipping'],
    paymentMethod: null,
    options: {
    mode: 'payment',
    amount: 1099,
    currency: 'usd',
    paymentMethodCreation: 'manual',
    },
    error: null,
    intent: null,
    useConfirmationToken: true,
    confirmationToken: null,
    confirmationTokenParams: null,
    success: false,
  }),
  methods: {
   async buildIntentPayload() {
      const payload = {
        confirm: true,
        amount: this.options.amount,
        currency: this.options.currency,
        automatic_payment_methods: {enabled: true},
        return_url: `${window.location.origin}/success`,
        use_stripe_sdk: true
      }
      if (this.useConfirmationToken) {
        const token = this.confirmationToken !== null ? this.confirmationToken : await this.makeConfirmationToken()
        payload.confirmation_token = token.id
        // payload.confirmation_token = 'ctoken_1PctYNIlCeH6bP8RpaEISW04'
      } else {
        const pm = this.paymentMethod !== null ? this.paymentMethod : await this.makePM()
        payload.payment_method = pm.id
        payload.mandate_data = {
          customer_acceptance: {
            type: 'online',
          }
        }
      }
      console.log(payload);
      return payload
    },
    addressListener(event) {
      console.log(event);
    },
    async mountElement() {
      this.elements = this.$stripe.elements(this.options)
      this.paymentElement = await this.elements.create('payment')
      this.paymentElement.mount('#payment-element-finalize')
      // Creating/mounting address element
      this.addressElement = this.elements.create('address', this.addressOptions)
      this.addressElement.mount('#address-element')
      this.addressElement.on('change', (ev) => {
        if (ev.complete) {
            const tokenPayload = {}
            tokenPayload[ev.elementMode] = ev.value
            this.confirmationTokenParams = tokenPayload
          }
        })
    },
    async submitPayment() {
      const {error: submitError} = await this.elements.submit()
      if (submitError) {
        this.error = submitError
        return
      }
      const payload = await this.buildIntentPayload()
      const response = await this.$axios.$post('/payment_intents/create_confirm/', payload)
      this.handleResponse(response)
    },
    setCurrency(currency) {
      console.log(currency);
      this.options.currency = currency
    },
    async makeConfirmationToken() {
      const {error, confirmationToken} = await this.$stripe.createConfirmationToken({
        elements: this.elements,
        params: {
          return_url: `${window.location.origin}/success`,
          shipping: {
            name: 'Jenny Rosen',
            address: {
              line1: '1234 Main Street',
              city: 'San Francisco',
              state: 'CA',
              country: 'US',
              postal_code: '94111',
            },
          },
        }
      })
      if (error) {
        this.error = error
        return;
      }
      this.confirmationToken = confirmationToken
      return confirmationToken
    },
    async makePM() {
      const {error, paymentMethod} = await this.$stripe.createPaymentMethod({
          elements: this.elements,
          params: {
            billing_details: {
              name: 'William Wombat'
            }
          }
        })
        if (error) {
          this.error = error
          return
        }
        this.paymentMethod = paymentMethod
        return paymentMethod
    },
    async handleResponse(response) {
      if (response.error) {
        this.error = response.error

      } else if (response.intent.status === 'requires_action') {
        const {error, paymentIntent} = await this.$stripe.handleNextAction({clientSecret: response.intent.client_secret})
        if (error) {
          this.error = error
        } else {
          this.intent = paymentIntent
          console.log(paymentIntent);
        }
      } else {
        console.log('No additional action required');
        this.success = true
      }
    }
  }
}
</script>

