<template>
  <div>
    <v-row justify="center">
      <v-col align-items="center">
        <p class="text-h2">Embedded Checkout</p>
        <v-divider></v-divider>
        <p>Following <a href="https://site-admin.stripe.com/docs/payments/accept-a-payment?platform=web&ui=embedded-checkout">this doc</a></p>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="12" sm="12" md="6" lg="4">
        <v-card flat>
          <v-card-title>Configure Options</v-card-title>
          <v-card-text>
            <v-form>
              <p class="text-h6">Select Prices</p>
              <v-row>

                <v-col
                  v-for="price in prices"
                  :key="price.id">

                  <v-checkbox
                  v-model="selected_prices"
                  :label="price.name"
                  :value="price.id"
                  :hint="price.type"
                  persistent-hint
                  @click="check_mode"
                  ></v-checkbox>
                </v-col>
              </v-row>
              <p class="text-h6 my-8">Allow Promo Codes</p>
              <v-row>
                <v-col>
                  <v-switch
                   v-model="session_options.allow_promotion_codes"
                   label="Allow promotion codes"

                  ></v-switch>
                </v-col>
              </v-row>
            </v-form>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-btn color="primary" class="my-4" @click="createSession">Create Session</v-btn>
          </v-card-actions>
        </v-card>

      </v-col>
      <v-col cols="12" sm="12" md="6" lg="8">
        <div id="checkout" class="pa-8 indigo  white--text">
         Checkout Loaded Here
        </div>
      </v-col>
      <v-col cols="12" sm="12" class="mt-12">
        <ErrorAlert :error="error" />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import ErrorAlert from '~/components/stripe/ErrorAlert.vue';

export default {
  components: { ErrorAlert },
  data: () => ({
      localStripe: null,
      error: null,
      session: null,
      session_options: {
          line_items: [],
          mode: 'payment',
          ui_mode: 'embedded',
          return_url: `${window.location.origin}/success`,
          allow_promotion_codes: false
      },
      prices: {
        one_time: {
          name: 'Gus the Chubby Wombat',
          id: 'price_1McGYcIlCeH6bP8RjvYVPlbS',
          type: "One Time Price"
        },
        recurring: {
          name: 'Ethiopia - Yirgacheffe',
          id: 'price_1NO7jZIlCeH6bP8RLlkjxVEL',
          type: "Recurring Price"
        }
      },
      selected_prices: [],
  }),
  methods: {
    check_mode() {
      const is_sub_mode = this.selected_prices.includes(this.prices.recurring.id)
      if (is_sub_mode) {
        this.session_options.mode = 'subscription'
      } else {
        this.session_options.mode = 'payment'
      }
    },
    build_line_items() {
      this.selected_prices.forEach((price) => {
        const item = {
          price, quantity: 1
        }
        this.session_options.line_items.push(item)
      })
    },
    async createSession() {
        const url = '/checkout_sessions/create_embedded/';
        try {
          this.build_line_items()
          const { secret } = await this.$axios.$post(url, this.session_options);
          console.log(secret);
          const checkout = await this.$stripe.initEmbeddedCheckout({clientSecret: secret})
          checkout.mount('#checkout')
        } catch (error) {
          this.error = error
        }
    }
  },

}
</script>

