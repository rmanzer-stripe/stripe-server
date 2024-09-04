<template>
  <v-card>
    <v-img
          class="white--text align-end"
          height="300px"
          src="https://images.pexels.com/photos/225502/pexels-photo-225502.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
          gradient="to top, rgba(0,0,0,0.5), rgba(0,0,0,0.2)"
          >
    <v-card-title class="text-h3">Welcome to Supermanzer</v-card-title>
    <v-divider color="white"></v-divider>
    <v-card-subtitle class="text-h5">Helping you build your software dreams since 2023</v-card-subtitle>
  </v-img>
  <v-card-text>
    <p class="text-h4">Custom Software Design & Development</p>
    <p class="text-h6">We offer a variety of custom solutions to meet your business needs.  Use the form below to select from the menu of options and submit to receive a service quote</p>
    <v-divider class="my-8"></v-divider>
    <v-row justify="center">
      <v-col cols="12" sm="6">
        <product-info :price="prices[0]" />
      </v-col>
      <v-col cols="12" sm="6">
        <v-form>
          <p class="text-h5">Select Options</p>
          <v-row>
            <v-col cols="12" sm="4" v-for="price in prices" :key="price.id">
              <product-checkbox
                :price="price"
                @selected-product="adjustSelected" />
            </v-col>
          </v-row>
          <v-row justify="center">
            <v-text-field
              v-model="email"
              prepend-inner-icon="mdi-email"
              label="Email"
              hint="Provide an email where we can send the quote for our services"
              persistent-hint

              ></v-text-field>
          </v-row>
        </v-form>
      </v-col>
      <v-col cols="12" sm="6" v-if="quote !== null">
        <stripe-object-view  :stripeObject="quote" />
      </v-col>
    </v-row>
  </v-card-text>
  <v-divider class="my-8"></v-divider>
  <v-card-actions>
    <v-row justify="space-around" class="my-4">
      <v-btn color="green" dark @click="generateQuote">Generate Quote</v-btn>
      <v-btn v-if="readyToAccept" color="primary" @click="acceptQuote">Accept Quote</v-btn>
    </v-row>
  </v-card-actions>
  </v-card>
</template>

<script>
import StripeObjectView from '~/components/stripe/StripeObjectView.vue'
import ProductCheckbox from '~/components/supermanzer/ProductCheckbox.vue'
import ProductInfo from '~/components/supermanzer/ProductInfo.vue'
export default {
  name: 'SupermanzerBilling',
  components: { ProductCheckbox, StripeObjectView, ProductInfo },
  data: () => ({
    prices: [],
    services_selected: [],
    email: null,
    quote: null,
  }),
  computed: {
    lineItems() {
      return this.services_selected.map((x) => {
        return {price: x}
      })
    },
    readyToAccept() {
      if (this.quote !== null && this.quote.status === "open") {
        return true
      } else {
        return false
      }
    }
  },
  async created() {
    const url = 'supermanzer/prices/'
    const response = await this.$axios.$get(url)
    if (response.data) {
      this.prices = response.data.reverse()
    }
  },
  methods: {
    adjustSelected({price, selected}) {
      if (selected) {
        this.services_selected.push(price)
      } else {
        this.services_selected = this.services_selected.filter(x => x !== price)
      }
    },
    async generateQuote() {
      const url = 'supermanzer/quotes/'
      const payload = {
        email: this.email,
        line_items: this.lineItems
      }
      this.quote = await this.$axios.$post(url, payload)
      this.services_selected = []
      this.email = null
    },
    async acceptQuote() {
      if (this.quote !== null) {
        const url = `supermanzer/quotes/${this.quote.id}/accept/`
        this.quote = await this.$axios.$post(url)
      } else {
        console.log("No quote associted");
      }
    }
  }
}
</script>

