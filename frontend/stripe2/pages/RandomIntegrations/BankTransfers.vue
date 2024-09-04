<template>
  <v-row justify="center">
    <v-col cols="12" sm="12" >
      <v-row class="my-4" justify="space-around">
          <v-form class="my-2">
            <v-row>
              <v-col>
                <v-text-field v-model="amount" type="number" label="Amount to transfer" prepend-icon="mdi-currency-usd"></v-text-field>
              </v-col>
              <v-col>
                <v-select label="Currency" v-model="currency" :items="currencies"></v-select>
              </v-col>
              <v-col>
                <div id="payment-element"></div>
              </v-col>
            </v-row>
          </v-form>
          <error-alert :error="error" />
        </v-row>
      <v-form class="my-8">
        <v-row justify="space-around" class="my-6">
          <v-btn class="primary" @click="retrieveCustomer">Get Customer</v-btn>
          <v-btn v-if="hasPI" class="indigo lighten-1 white--text" @click="refreshIntent">Refresh PI</v-btn>
          <v-btn v-else class="green darken-2 white--text" @click="createPaymentIntent">Create PI</v-btn>
          <v-btn class="blue lighten-4" @click="mountElement">Mount Element</v-btn>
          <v-btn class="deep-purple white--text" @click="confirmPayment">Confirm Payment</v-btn>

        </v-row>
      </v-form>
      <v-row>
        <v-col cols="12" sm="12" md="6">
          <stripe-object-view :stripe-object="myObject" />
        </v-col>
        <v-col cols="12" sm="12" md="6">
          <p class="text-h5">Payment Intents requiring funding</p>
          <p class="">Select one or more Payment Intents to fund the transfer</p>
          <select-data-table :headers="table_headers" :items="payments_need_funding" :single-select="false" :loading="payments_need_funding.length === 0 " @selected="setSelected" />
          <v-row >
            <v-col>
              <v-text-field v-model="amount_to_fund" type="number" label="Amount to fund" prepend-icon="mdi-currency-usd" class="mx-8"></v-text-field>
            </v-col>
            <v-col>
              <v-btn class="amber darken-4 white--text" @click="fund_transfers">Fund Transfers</v-btn>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
import ErrorAlert from '~/components/stripe/ErrorAlert.vue'
import SelectDataTable from '~/components/stripe/SelectDataTable.vue'
import StripeObjectView from '~/components/stripe/StripeObjectView.vue'
export default {
  components: { StripeObjectView, ErrorAlert, SelectDataTable },
  props: {
    successUrl: {type: String, required: false, default: ''}
  },
  data: () => ({
    customer: null,
    amount: 1099,
    currency: 'usd',
    currencies: ['usd', 'eur', 'gbp'],
    paymentIntent: null,
    error: null,
    elements: null,
    paymentElement: null,
    cashBalance: null,
    appearance: {},
    payments_need_funding: [],
    table_headers: [
      {text: 'ID', value: 'id'},
      {text: 'Status', value: 'status'},
      {text: 'Amount', value: 'amount'},
      {text: 'Customer', value: 'customer'},
      {text: 'Next Action', value: 'next_action.type'}
    ],
    selected_intents: [],
    amount_to_fund: 0
  }),
  computed: {
    myObject() {
      if (this.cashBalance != null) {
        return this.cashBalance
      } else if (this.paymentIntent != null) {
        return this.paymentIntent
      } else if (this.customer != null) {
        return this.customer
      } else if (this.selected_intents.length > 0 ){
        return this.selected_intents
      }
       else {
        return null
       }
    },
    hasPI() {
      return this.paymentIntent !== null
    }
  },
  mounted(){
    this.needsFunding()
   },
  methods: {
   async retrieveCustomer() {
     const resp = await this.$axios.$get('/customers/', {
      expand: ['cash_balance']
     })
     this.customer = resp.results[0].data
   },
   async createPaymentIntent() {
      if (this.customer !== null) {
        const payload = {
        amount: this.amount,
        currency: this.currency,
        customer: this.customer.id,
        payment_method_types: ['customer_balance'],
        payment_method_data: {type: 'customer_balance'},
        payment_method_options: {
          customer_balance: {
            funding_type: 'bank_transfer',
            bank_transfer: {
              type: 'us_bank_transfer'
            }
          }
        }
      }
      const {intent} = await this.$axios.$post('/payment_intents/', payload)
      this.paymentIntent = intent
      } else {
        this.error = {type: "missing_parameter", message: "Please load the customer first"}
      }

   },

   async refreshIntent() {
    const url = `/payment_intents/${this.paymentIntent.id}`
    this.paymentIntent = await this.$axios.$get(url)
   },
   mountElement() {
    if (this.paymentIntent.client_secret) {
      this.elements = this.$stripe.elements({clientSecret: this.paymentIntent.client_secret})
      this.paymentElement = this.elements.create('payment')
      this.paymentElement.mount('#payment-element')
    } else {
      this.error = {
        code: 'missing_intent',
        type: 'error',
        request: "this one",
        message: "no payment intent client secret was provided"
      }
    }
   },
   async confirmPayment() {
    const {error} = await this.$stripe.confirmPayment({
      elements: this.elements,
      confirmParams: {
        return_url: this.successUrl
      }
    });
    if (error) {
      this.error = error
    }
   },
   fund_transfers() {
    this.selected_intents.forEach(
      async (pi) => {
          await this.fund_transfer(pi)
        }
      )
   },
   async fund_transfer(pi){
    const url = `/customers/${pi.customer}/fund_cash_balance/`

    const payload = {
      amount: this.amount_to_fund,
      currency: pi.currency,
      reference: pi.next_action.display_bank_transfer_instructions.reference
    }
    // await console.log(url, payload);
    const {cash_balance} = await this.$axios.$post(url, payload)
    if (cash_balance) {
      this.cashBalance = cash_balance
      this.paymentIntent = pi
      await this.needsFunding()
    }

   },
   async needsFunding() {
    const pis = await this.$axios.$get('/payment_intents/needs_funding/')
    this.payments_need_funding = pis.map((x) => x.data)
   },
   setSelected(ev) {
    this.selected_intents = ev
   }
  }
}
</script>

