<template>
  <v-card>
    <v-dialog
      v-model="dialog"
      persistent
      width="500"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="red lighten-2"
          dark
          v-bind="attrs"
          v-on="on"
        >
          Click Me
        </v-btn>
      </template>

      <v-card>
        <v-card-title class="text-h5 grey lighten-2">
          Privacy Policy
        </v-card-title>

        <v-card-text>
          <div id="payment-element"></div>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="dialog = false"
          >
            Mount
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
export default {
 data: () => ({
  dialog: false,
  intentOptions: {
    amount: 2099,
    currency: 'usd',
    automatic_payment_methods: {enabled: true}
  },
 }),
 methods: {
  mountElement() {
    if (this.payment_intent) {
      this.elements = this.$stripe.elements(
        {clientSecret: this.payment_intent.client_secret}
      )
    } else {
      this.elements = this.$stripe.elements({
        mode: 'payment',
        currency: this.intentOptions.currency,
        amount: this.intentOptions.amount
      })
    }
    this.payment_element = this.elements.create('payment')
    this.payment_element.mount('#payment-element')
  },
 }
}
</script>
