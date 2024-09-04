<template>
  <v-container>
    <v-row justify="center">
      <v-card width="80%">
        <v-card-text>
          <v-card-title>Affirm Payment</v-card-title>
          <v-card-subtitle>Go into debt faster, with higher fees!</v-card-subtitle>
          <v-divider></v-divider>
          <v-form>
            <v-text-field v-model="amount" label="Set Amount" hint="Set an amount greater than $100 USD"></v-text-field>
            <v-select
              v-model="currency"
              label="Select Currency"
              :items="currencies"
              item-text="value"
              item-value="key"
            ></v-select>
          </v-form>
          <error-alert :error="error" />
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="my-4">
          <v-row justify="space-around">
            <v-btn color="blue lighten-2" class="white--text" @click="createIntent">Create Intent</v-btn>
            <v-btn color="purple" class="white--text" :disabled="intent === null" @click="confirmIntent">Confirm Intent</v-btn>
          </v-row>
        </v-card-actions>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>
import ErrorAlert from '~/components/stripe/ErrorAlert.vue'
export default {
  components: { ErrorAlert },
  name: 'AffirmPayment',
  data: () => ({
    amount: 50000,
    currency: 'usd',
    currencies: [
      {
        key: 'usd',
        value: "USD"
      },
      {
        key: 'cad',
        value: "CAD"
      },
      {
        key: "eur",
        value: "EUR"
      }
    ],
    intent: null,
    error: null,
  }),
  methods: {
    async createIntent() {
      const url = '/payment_intents/'
      const payload = {
        amount: this.amount,
        currency: this.currency,
        payment_method_types: [
          'affirm'
        ]
      }
      const { intent, error } = await this.$axios.$post(url, payload)
      if (error) {
        this.error = error
        return
      }
      this.intent = intent
    },
    async confirmIntent() {
      if (this.intent) {
        const result = await this.$stripe.confirmAffirmPayment(
          this.intent.client_secret,
          {
            payment_method: {
              // Billing information is optional but recommended to pass in.
              billing_details: {
                email: 'jenny@rosen.com',
                name: 'Jenny Rosen',
                address: {
                  line1: '1234 Main Street',
                  city: 'San Francisco',
                  state: 'CA',
                  country: 'US',
                  postal_code: '94111',
                },
              },
            },

            // Shipping information is optional but recommended to pass in.
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
            // Return URL where the customer should be redirected after the authorization.
            return_url: `${window.location.origin}/success`,
          })
          console.log(result);
      } else {
        this.error = {message: 'Please generate an intent with a client secret', code: 'no_intent'}
      }
    }
  }
}
</script>

