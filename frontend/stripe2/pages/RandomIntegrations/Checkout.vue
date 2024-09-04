<template>
  <v-container class="mx-auto">
    <v-card :loading="processing">

        <v-card-title>Buy this cool product</v-card-title>
        <v-card-subtitle>It is pretty darn cool after all</v-card-subtitle>
        <v-card-text>
          You can use this to purchase a single Tangible Wombat for $180.  You can subscribe to receive one tangible wombat a month for $120/month.  Or you can save your payment method for use for later wombat purchases.

          <v-form>
            <v-text-field v-model="quantity" type="number" ></v-text-field>
            <v-select
              v-model="mode"
              :hint="`${mode.text}, ${mode.value}`"
              :items="modes"
              label="Select"
              persistent-hint
              return-object
              single-line
            ></v-select>
            <v-select
              v-model="customer_email"
              :items="customer_emails"
              label="Set Customer email"
            ></v-select>
          </v-form>
        </v-card-text>

      <v-card-actions>
        <v-row justify="end" class="ma-6">
          <v-btn :disabled="processing" :loading="processing" color="blue-grey lighten-2 white--text" @click="createSession">
            <v-icon left> mdi-currency-usd</v-icon>
            Check Out</v-btn>
        </v-row>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name:"StripeCheckout",
  data: () => ({
    success_url: `${window.location.origin}/success`,
    cancel_url: `${window.location.origin}/cancel`,
    payment_price: 'price_1OHUBPIlCeH6bP8ROuMQ6COV', // USD
    // payment_price: 'price_1O0oIPIlCeH6bP8RUf3ZDll6', // EUR
    // subscription_price: 'price_1MYe5BIlCeH6bP8Rq4N9xQGK',
    subscription_price: 'price_1OEy2ZIlCeH6bP8RFcnjDkZr',
    mode: {value: 'payment', text: "Buy single wombat"},
    modes: [
      {value: 'payment', text: "Buy single wombat"},
      {value: 'subscription', text: "Multi-currency Price"},
      {value: 'setup', text: "Save payment method for future wombat purchases"}
    ],
    quantity: 0,
    processing: false,
    trial_days: 0,
    customer_emails: [
      'test@example.com',
      'test+location_GB@example.com',
      'test+location_FR@example.com',
      'test+location_CA@example.com'
    ],

    customer_email: null
  }),
  computed: {
    checkoutPrice() {
      if (this.mode.value !== 'setup') {
        return (this.mode.value === 'payment' ? this.payment_price : this.subscription_price)
      }
      return ''
    }
  },
  methods: {
   async createSession() {
    this.processing = true
     const payload = {
      mode: this.mode.value,
      success_url: `${this.success_url}?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: this.cancel_url,
      // billing_address_collection: 'required',
      // shipping_address_collection: {allowed_countries: ['US', 'CA', 'GB']},
      payment_method_collection: 'always',
      // payment_method_data: {
      //   allow_redisplay: 'always'
      // },
      payment_intent_data: {
        setup_future_usage: 'off_session'
      },
      payment_method_options: {
        card: {
          setup_future_usage: 'off_session'
        }
      },
      saved_payment_method_options: {
        payment_method_save: "enabled",
        allow_redisplay_filters: ['always', 'limited', 'unspecified'],
      },
      customer_creation: 'if_required',
      // customer: 'cus_PpNUvNttJy8aKS',
      customer_update: {
        name: 'auto',
        address: 'auto'
      },
      custom_fields: [
        {
          key: "engraving",
          label: {type: "custom", custom: "Personalized engraving"},
          type: 'text'
        }
      ],
      custom_text: {
        terms_of_service_acceptance: {
          message: "We reserve the right to throw wombats at you"
        }
      },
      consent_collection: {
        terms_of_service: 'required'
      }
     }
     if (this.mode.value !== 'setup') {
      payload.line_items = [
        {
          price: this.checkoutPrice,
          quantity: this.quantity
        }
      ]
     } else {
      payload.payment_method_types = [
        'card',
        'sepa_debit',
        'ideal',
        'sofort',
        'amazon_pay'
      ]
     }
     if (this.trial_days > 0) {
      payload.subscription_data.trial_period_days = this.trial_days
     }
     if (this.mode.value === 'subscription') {
        delete payload.payment_intent_data
        delete payload.payment_method_options
     }
     if (this.mode.value === 'subscription' && this.customer_email !== null) {
        payload.customer_email = this.customer_email
     }
     console.log(payload);
     const {url, error} = await this.$axios.$post('/checkout_sessions/', payload)
     if (error) {
        console.error(error)
        this.processing = false
     } else {
      window.location.replace(url)
      // console.log(url);
     }
    }
  }
}
</script>
