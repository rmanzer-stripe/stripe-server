<template>
  <v-container class="mx-auto">
    <v-card :loading="processing">

        <v-card-title>Buy this cool product</v-card-title>
        <v-card-subtitle>It is pretty darn cool after all</v-card-subtitle>
        <v-card-text>
          You can use this to purchase a single Tangible Wombat for $180.  You can subscribe to receive one tangible wombat a month for $120/month.  Or you can save your payment method for use later.

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
  data: () => ({
    success_url: `${window.location.origin}/success`,
    payment_price: 'price_1McGYpIlCeH6bP8RwL3H6puY',
    subscription_price: 'price_1MYe5BIlCeH6bP8Rq4N9xQGK',
    mode: {value: 'payment', text: "Buy single wombat"},
    modes: [
      {value: 'payment', text: "Buy single wombat"},
      {value: 'subscription', text: "Wombat Subscription"},
      {value: 'setup', text: "Save payment method for future wombat purchases"}
    ],
    quantity: 0,
    processing: false
  }),
  computed: {
    checkoutPrice() {
      if (this.mode.value !== 'setup') {
        return (this.mode.code === 'payment' ? this.payment_price : this.subscription_price)
      }
      return ''
    }
  },
  methods: {
   async createSession() {
    this.processing = true
     const payload = {
      mode: this.mode.code,
      success_url: this.success_url,
      cancel_url: this.success_url,
      // customer: 'cus_PpNUvNttJy8aKS',
      customer_update: {
        address: 'auto',
        name: 'auto'
      }
      // billing_address_collection: 'required',
     }
     if (this.mode.value !== 'setup') {
      payload.line_items = [
        {
          price: this.checkoutPrice,
          quantity: this.quantity
        }
      ]
     }
    //  console.log(payload);
     const {url, error} = await this.$axios.$post('/checkout_sessions/', payload)
     if (error) {
        console.error(error)
        this.processing = false
     } else {
      window.location.replace(url)
     }
    }
  }
}
</script>
