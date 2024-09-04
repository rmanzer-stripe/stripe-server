<template>
  <v-card class="my-8" flat>
        <v-img
          class="white--text align-end"
          height="300px"
          src="https://images.pexels.com/photos/955733/pexels-photo-955733.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
          gradient="to top, rgba(0,0,0,0.5), rgba(0,0,0,0.2)"
          >
          <v-card-title>2 Step Confirmation - Confirmation Tokens</v-card-title>
          <v-card-subtitle>Based on <a href="https://stripe.com/docs/payments/build-a-two-step-confirmation">this doc</a></v-card-subtitle>
        </v-img>
        <v-card-text>
          <v-card-title>Checkout</v-card-title>
          <v-card-subtitle>Provide Payment Details</v-card-subtitle>
          <v-form class="mx-10" @input="update_options">
            <v-row>
              <v-col>
                <v-text-field  v-model="options.amount" label="Amount to Charge"></v-text-field>
              </v-col>
              <v-col>
                <v-select v-model="options.currency" :items="currencies"  label="Select Currency"></v-select>
              </v-col>
            </v-row>


            <div id="payment-element"></div>
            <error-alert :error="error" />
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="">
          <v-row justify="space-around" class="my-6">
            <v-btn class="teal darken-3 white--text" @click="mount_element">Mount Element</v-btn>
            <v-btn class="indigo darken-3 white--text" :disabled="loading" @click="submit" >Submit</v-btn>
          </v-row>
        </v-card-actions>
      </v-card>
</template>

<script>
import ErrorAlert from '../ErrorAlert.vue'
export default {
  components: { ErrorAlert },
  data: () => ({
    elements: null,
    payment_element: null,
    currencies: ['usd', 'cad', 'eur', 'gbp'],
    options: {
      mode: 'payment',
      amount: 1299,
      currency: 'usd',
      paymentMethodCreation: 'manual'
    },
    error: null,
    loading: false,
    token: null,
    allowed_brands: ['visa', 'mastercard'],
    card_brands: []
  }),
  watch: {
    options() {
      this.update_options(this.options)
    }
  },
  created() {
    this.elements = this.$stripe.elements(this.options)
  },
  methods: {
  async mount_element() {
      this.payment_element = await this.elements.create('payment', {fields: {address: 'never'}})
      this.payment_element.mount('#payment-element')
    },
    update_options(ev) {
      console.log(ev);
    },
    async submit() {
      this.loading = true

      const {error: submitError} = await this.elements.submit()
      if (submitError) {
        this.error = submitError
        return;
      }

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

      } else {
          this.token = confirmationToken
          console.log(confirmationToken);
          // const brand = this.token.payment_method_preview.card.brand
          // const funding = this.token.payment_method_preview.funding
          // if (!this.allowed_brands.includes(brand) || funding !== "credit") {
          //   this.error = {
          //     code: "unsupported_card_brand",
          //     type: "invalid_request",
          //     message: "We only support Visa and MasterCard credit cards.\n\nNo Discover, Amex, or pre-paid cards are accepted at this establishment",
          //     request: "wouldn't you like to know"
          //   }
          //   return;
          // }
          this.fetchAndRenderSummary(confirmationToken)
      }
    },
    async fetchAndRenderSummary(token) {
      const response = await this.$axios.$post('/confirmation-tokens/summary/', {
        token_id: 'ctoken_1PctYNIlCeH6bP8RpaEISW04'
      });
      console.log(response);
    }
  },

}
</script>
