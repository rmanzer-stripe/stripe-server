<template>
  <div>
    <v-row justify="center" class="my-4">
      <v-col cols="12" lg="12">
        <p class="text-h2">Billing Meters</p>
        <v-divider></v-divider>
        <p class="text-h5">Setting up usage based billing following the new <a target="_blank" href="https://docs.stripe.com/billing/subscriptions/usage-based/implementation-guide">guide</a></p>
      </v-col>
    </v-row>
    <v-row>
      <v-alert
       v-model="error.display"
       border="left"
       colored-border
       type="error"
       elevation="2"
       dismissible
      >
      <p class="text-h4">{{ error.headline }}</p>
      <v-divider></v-divider>
      <p>{{ error.text }}</p>
    </v-alert>
    </v-row>
    <v-row>
      <v-col cols="12" sm="6" md="3" lg="2">
        <v-form>
          <p>
             Select or Create Meter
             <a v-if="meter === null" href="https://docs.stripe.com/billing/subscriptions/usage-based/recording-usage#configuring-meter" target="_blank">
               <v-icon right dense>mdi-help</v-icon>
             </a>
             <v-icon v-else class="green--text">
              mdi-check-bold
             </v-icon>
          </p>
          <v-select
            v-model="meter"
            :items="meters"
            item-text="display_name"
            item-value="id"
            label="Billing Meter"
            single-line
            return-object
            @change="getPrices"
          ></v-select>
          <v-text-field
            v-model="meter_data.display_name"
            label="Display name"
            hint="A friendly readable name for your meter"
            :disabled="meter !== null"></v-text-field>
          <v-text-field
            v-model="meter_data.event_name"
            label="Event name"
            hint="The name of the meter event to record usage"
            :disabled="meter !== null"
          ></v-text-field>
          <v-btn :disabled="meter !== null" @click="createMeter" color="primary">Create Meter</v-btn>
        </v-form>
      </v-col>
      <v-col cols="12" sm="6" md="3" lg="2">
        <p>
          Select or Create a Customer

          <a v-if="customer === null" href="https://docs.stripe.com/billing/subscriptions/usage-based/implementation-guide?dashboard-or-api=api#test-send-usage" target="_blank">
               <v-icon right dense>mdi-help</v-icon>
             </a>
             <v-icon v-else class="green--text">
              mdi-check-bold
             </v-icon>
        </p>
        <customer-select
        v-on:customer-selected="setCustomer"
        />

        <v-text-field
         v-model="customer_data.name"
         label="Customer Name"
         hint="A useful name to identify this customer"
         :disabled="customer !== null"
        ></v-text-field>
        <v-text-field
          v-model="customer_data.email"
          label="Customer Email"
          hint="Just an email address"
          placeholder="joey.meters@bufo.io"
          :disabled="customer !== null"
        ></v-text-field>
        <v-btn :disabled="customer !== null" @click="createCustomer" color="primary">Create Customer</v-btn>
      </v-col>
      <v-col cols="12" sm="6" md="3" lg="2">
        <p>
          Select or Create a Price
          <a v-if="price === null" href="https://docs.stripe.com/billing/subscriptions/usage-based/implementation-guide?dashboard-or-api=api#test-send-usage" target="_blank">
               <v-icon right dense>mdi-help</v-icon>
             </a>
             <v-icon v-else class="green--text">
              mdi-check-bold
          </v-icon>
        </p>
        <v-select
          v-model="price"
          :items="prices"
          item-text="nickname"
          item-value="id"
          single-line
          return-object
        ></v-select>
        <v-text-field
          v-model="price_data.lookup_key"
          label="Lookup key"
          hint="A string used to look up a particular price"
          :disabled="price !== null"
        ></v-text-field>
        <v-text-field
          v-model="price_data.nickname"
          label="Description"
          hint="A user-facing string to represent this price"
          :disabled="price !== null"
        ></v-text-field>
        <v-text-field
          v-model="price_data.unit_amount"
          label="Unit Amount"
          hint="Cost per unit"
          :disabled="price !== null"
        ></v-text-field>
        <v-btn
         :disabled="price !== null"
         @click="createPrice"
         color="primary"
        >Create Price</v-btn>
      </v-col>
      <v-col cols="12" sm="6" md="3" lg="2">
        <v-btn
          :disabled="subscription !== null"
          class="teal darken-2 white--text"
          @click="createSubscription"
        >Create Subscription</v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import CustomerSelect from '../stripe/CustomerSelect.vue'
export default {
  name: 'BillingMeters',
  components: { CustomerSelect },
  data: () => ({
    meter_data: {
      display_name: "",
      event_name: "",
      default_aggregation: {"formula": "sum"},
      customer_mapping: {"event_payload_key": "stripe_customer_id", type: "by_id"},
      value_settings: {"event_payload_key": "value"}
    },
    meter: null,
    customer: null,
    price: null,
    subscription: null,
    meters: [],
    prices: [],
    customer_data: {
      name: '',
      email: ''
    },
    error: {
      headline: '',
      text: '',
      display: false
    },
    price_data: {
      lookup_key: '',
      unit_amount: 25,
      nickname: ''
    },
    stripe_account: null,
  }),
  created() {
    this.getMeters()
    this.setAccount()
  },
  methods: {
    setAccount() {
      this.stripe_account = this.$store.state.account.id
    },
    async getMeters() {
      const payload = {account: this.stripe_account}
      const {meters} = await this.$axios.$get('/billing_meters/', payload)
      this.meters = meters.data
    },
    async createMeter() {
      if (this.meter_data.display_name !== "") {
        const payload = {...this.meter_data, ...{account: this.stripe_account}}
        const {meter} = await this.$axios.$post('/billing_meters/', payload)
        this.meter = meter
        await this.getMeters()
      }
    },
    setCustomer(customer) {
      // console.log(customer);
      this.customer = customer
    },
    async createCustomer() {
      const payload = {...this.customer_data, ...{account: this.stripe_account}}
      this.customer = await this.$axios.$post('/customers/', payload)
    },
    async getPrices() {
      console.log("getPrices called");

      if (this.meter !== null) {
        const payload = {
          params: {
            type: 'recurring',
            recurring: {
              meter: this.meter.id
            }
          }
        }
        const {prices} = await this.$axios.$get('/prices', payload)
        this.prices = prices.data
      } else {
        this.error.headline = 'No Meter'
        this.error.text = 'Select a meter before fetching or creating Prices'
        this.error.display = true
      }
    },
    async createPrice(){
      const defaults = {
        currency: 'usd',
        billing_scheme: 'per_unit',
        recurring: {
          interval: 'month',
          'usage_type': 'metered',
          'meter': this.meter.id
        },
        product_data: {
          name: 'Supermanzer Usage'
        }
      }
      const payload = {...defaults, ...this.price_data}
      const {price} = await this.$axios.$post('/prices/', payload)
      this.price = price
    },
    async createSubscription() {
      const payload = {
        customer: this.customer.id,
        items:[
          {price: this.price.id}
        ],
        expand: ['latest_invoice.payment_intent'],
        account: this.stripe_account
      }
      const {subscription} = await this.$axios.$post('/subscriptions/', payload)
      this.subscription = subscription
    }
  }
}
</script>
