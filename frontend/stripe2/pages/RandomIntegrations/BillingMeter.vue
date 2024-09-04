<template>
  <v-row>
    <v-img
    src="https://images.pexels.com/photos/942316/pexels-photo-942316.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
    :height="300"
    gradient="to top, rgba(0,0,0,0.5), rgba(0,0,0,0.8)"
    class="white--text align-end"
    position="top center"
    >
    <p class="text-h2">Billing with Meters</p>
    </v-img>
    <v-col cols="12" md="6" sm="12">
      <v-card>
        <v-card-text>
          <v-form>
            <p class="text-h4">Create or Select a Billing Meter</p>
            <v-select
              v-model="billing_meter"
              :items="meters"
              :hint="`${billing_meter.display_name}`"
              item-text="display_name"
              item-value="event_name"
              persistent-hint
              return-object
              single-line
              ></v-select>
            <v-text-field
            v-model="meter_data.display_name"
            label="Display Name"
            hint="A human readable name to identify this meter"
            persistent-hint
            ></v-text-field>
            <v-text-field
            v-model="meter_data.event_name"
            label="Event Name"
            hint="A snake_case event name"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-row class="my-4" justify="center">
            <v-btn @click="createMeter" color="primary">Create Meter</v-btn>
          </v-row>
        </v-card-actions>
      </v-card>
      <v-card class="mt-4">

        <v-card-text>
          <v-select></v-select>
          <stripe-object-view :stripe-object="price_data"></stripe-object-view>
        </v-card-text>
        <v-card-actions>

          <v-row justify="space-around">
            <v-btn
              color="teal darken-2"
              class="white--text"
              @click="createPrice">Create Price</v-btn>
              <v-tooltip bottom>

              <template v-slot:activator="{on, attrs}">
                <v-btn
                  color="indigo darken-2"
                  class="white--text"
                  @click="createSub"
                  v-bind="attrs"
                  v-on="on"
                >Create Sub</v-btn>
            </template>
            <span v-text="`For Customer ${customer}`"></span>
            </v-tooltip>
          </v-row>
        </v-card-actions>
      </v-card>
    </v-col>
    <v-col cols="12" md="6" sm="12">
      <stripe-object-view
        v-for="(object, i) in objects"
        :key="i"
        :stripe-object="object"
        class="my-2"
        />
    </v-col>
  </v-row>
</template>

<script>
import StripeObjectView from '~/components/stripe/StripeObjectView.vue'

export default {
  components: { StripeObjectView },
  data: () => ({
    meter_data: {
      display_name: "",
      event_name: "",
      default_aggregation: {"formula": "sum"},
      customer_mapping: {"event_payload_key": "stripe_customer_id", type: "by_id"},
      value_settings: {"event_payload_key": "value"}
    },
    billing_meter: {},
    prices: [],
    price: {},
    customer: 'cus_PudQkiAhwlIIVo',
    subscription: {},
    events: [],
    meters: null,
    price_data: {
      recurring: {
        interval: "month",
        "usage_type": "metered",
        "meter":  null,
      },
      product: 'prod_OTY0Ho5XSw3Mhf',
      currency: "usd",
      unit_amount: 1099,
      nickname: "Metered wombat"
    },
  }),
  computed: {
    objects() {
      return [
        this.billing_meter,
        this.price,
        this.customer,
        this.subscription,
        this.events
      ]
    }
  },
  async created() {
    await this.getCustomer()
    await this.getMeters()
    await this.getPrices()
  },
  methods: {
    async getCustomer() {
      const { data }  = await this.$axios.get(`/customers/${this.customer}/`)
      this.customer = data
    },
    async createMeter() {
      const payload = this.meter_data
      const {meter} = await this.$axios.$post('/billing_meters/', payload)
      this.billing_meter = meter
      await this.getMeters()
    },
    async getMeters() {
      const {meters} = await this.$axios.$get('/billing_meters/')
      this.meters = meters.data
      if (Object.keys(this.billing_meter).length === 0 ) {
        this.billing_meter = this.meters[0]
      }
    },
    async getPrices() {
      const payload = {usage_type: 'metered'}
      const { prices } = await this.$axios.$get('/prices/recurring/', payload)
      this.prices = prices
      if (Object.keys(this.price).length === 0) {
        this.price = prices[0]
      }
    },
    async createPrice() {
      const {price} = await this.$axios.$post('/prices/', this.price_data)
      console.log(price);
      this.price = price
    },
    async createSub() {
      const payload = {
        customer: this.customer,
        items: {
          price: this.price.id
        }
      }
      const {sub} = await this.$axios.$post('/subscriptions/', payload)
      this.subscription = sub
    }
  }
}

</script>
