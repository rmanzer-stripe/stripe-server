<template>
  <v-card flat>
    <v-card-title>2 Step Confirmation with Confirmation Tokens</v-card-title>
    <v-divider></v-divider>
    <v-card-subtitle>Using Confirmation Tokens to do things, and stuff!</v-card-subtitle>
    <v-card-text>
      <div v-if="token === null" id="payment-element"></div>
      <ConfirmationPage
      v-else
      :amount="elementOptions.amount"
      :currency="elementOptions.currency"
      :mode="elementOptions.mode"
      :confirmation-token="token" />
      <v-alert v-if="error !== null" type="error" outlined>
        {{ error }}
      </v-alert>
    </v-card-text>
    <v-card-actions>
      <v-row justify="space-around" class="my-4">
        <v-btn class="teal darken-2 white--text" @click="createMountPE">Mount Element</v-btn>
        <v-btn class=" amber darken-3 white--text" @click="createToken" :disabled="processing">Create Token</v-btn>
        <v-btn class="indigo darken-2 white--text" :disabled="processing" @click="createPaymentIntent">Submit Payment</v-btn>
      </v-row>
    </v-card-actions>
  </v-card>
</template>

<script>
import ConfirmationPage from '~/components/stripe/multiStep/ConfirmationPage.vue'
export default {
  components: { ConfirmationPage },
  data: () => ({
    elements: null,
    element: null,
    elementsOptions: {
      mode: 'payment',
      amount: 1099,
      currency: 'usd',
      paymentMethodCreation: 'manual',
      setupFutureUsage: 'off_session',
      captureMethod: 'automatic_async'
    },
    elementOptions: {
      type: 'tabs',
      radios: false,
      defaultCollapsed: false,
      spacedAccordionItems: false
    },
    returnUrl: `http://${window.location.host}/success`,
    error: null,
    intent: null,
    token: null,
    paymentSummary: null,
    processing: false
  }),
  methods: {
    createMountPE() {
      this.elements = this.$stripe.elements(this.elementsOptions)
      this.element = this.elements.create('payment', this.elementOptions)
      this.element.mount('#payment-element')
    },
    async createToken() {
      this.processing = true
      console.log("Set processing to True");
      const {error: submitError} = await this.elements.submit()
      if (submitError) {
        this.error = submitError
        return
      }

      const {error, confirmationToken} = await this.$stripe.createConfirmationToken({
        elements: this.elements,
        params: {
          return_url: this.returnUrl
        }
      })
      if (error) {
        this.error = error
        return
      }
      this.token = confirmationToken
      this.processing = false
    },
    async summarizePayment() {
      const response = await this.$axios.$post('/confirmation_tokens/summary/', {
        confirmation_token_id: this.token.id
      })
      // TODO: Do something with this   or not...this seems dumb
      this.paymentSummary = await response.json()
    },
    async createPaymentIntent() {
      const payload = {
        amount: this.elementsOptions.amount,
        currency: this.elementsOptions.currency,
        automatic_payment_methods: {
          enabled: true
        }
      }
      const { intent } = await this.$axios.$post('/payment_intents/', payload)
      console.log(intent);
    }
  }
}
</script>


