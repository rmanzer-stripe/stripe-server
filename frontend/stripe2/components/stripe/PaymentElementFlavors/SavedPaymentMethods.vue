<template>
  <v-card flat>
    <v-card-title>Saved Payment Methods</v-card-title>
    <v-card-subtitle>Use this to create and display saved payment methods in the the Payment Element</v-card-subtitle>
    <v-divider></v-divider>
    <v-card-text>
      <v-form>
        <p>Customer Data</p>
        <v-row>
          <v-col>
            <v-text-field v-model="customer_name" label="Customer Name"></v-text-field>
          </v-col>
          <v-col>
            <v-text-field v-model="customer_email" label="Customer Email"></v-text-field>
          </v-col>
        </v-row>
        <p>Intent Data</p>
        <v-row>
          <v-col>
            <v-switch v-model="intent_data.setup" :label="`Use SetupIntent ${intent_data.setup.toString()}`"></v-switch>
          </v-col>
          <v-col>
            <v-switch
              v-model="intent_data.require_cvc_recollection"
              :label="`Recollect CVC:${intent_data.require_cvc_recollection.toString()}`"
              :disabled="intent_data.setup"
              ></v-switch>
          </v-col>
          <v-col>
            <v-text-field v-model="intent_data.amount" label="Amount" :disabled="intent_data.setup"></v-text-field>
          </v-col>
          <v-col>
            <v-select v-model="intent_data.currency" :items="currencies" :disabled="intent_data.setup"></v-select>
          </v-col>
        </v-row>
        <v-divider class="my-6"></v-divider>
      </v-form>
      <p>Payment Element</p>
      <v-row>
        <v-col cols="12" sm="10" offset="1">
          <div id="payment">
            <v-alert type="info" text>
              Payment Element rendered here
            </v-alert>
          </div>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-actions>
      <v-row class="my-8" justify="space-around">
        <v-btn class="orange darken-4 white--text" @click="getOrCreateCustomer" :disabled="customer !== null">
          Create Customer
        </v-btn>
        <v-btn class="teal darken-4 white--text" @click="createSession" :disabled="customer_session !== null">
          Create Session
        </v-btn>
        <v-btn class="indigo darken-4 white--text" @click="createIntent" :disabled="intent !== null">
          Create Intent
        </v-btn>
        <v-btn class="purple darken-4 white--text" @click="mountElement" :disabled="element !== null">
          Mount Element
        </v-btn>
        <v-btn color="primary" @click="confirmIntent">Confirm Intent</v-btn>
      </v-row>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  data: () => ({
    elements: null,
    element: null,
    intent: null,
    intent_data: {
      setup: false,
      amount: 1099,
      currency: 'usd',
      require_cvc_recollection: false,
    },
    currencies: ['usd', 'eur', 'gbp'],
    customer_session: null,
    customer: null,
    customer_name: 'Saved PM',
    customer_email: 'saved.pm@bufo.io',
    stripe: null,
    stripe_account: null
  }),
  created() {
    this.setClient()
  },
  methods: {
    setClient() {
      this.stripe_account = this.$store.state.account
      this.stripe = window.Stripe(this.stripe_account.pk)
    },
    async getOrCreateCustomer() {
      this.setClient()
      const resp = await this.$axios.$get('/customers/', {params: {
         email: this.customer_email
    }})
      if (resp.customers.data.length > 0) {
        this.customer = resp.customers.data[0]
        return;
      }
      const {customer} = await this.$axios.$post('/customers/', {
        name: this.customer_name,
        email: this.customer_email,
        account: this.stripe_account.id
      })
      this.customer = customer
    },
    async createSession() {
      const url = `/customers/${this.customer.id}/create_session/`
      const {session} = await this.$axios.$post(url, {
        account: this.stripe_account.id
      })
      this.customer_session = session
    },
    async createIntent() {
      if (this.customer == null) {
        alert('Customer required. Please asign a customer first')
        return;
      }
      const params = {
        customer: this.customer.id,
        account: this.stripe_account.id}
      const url = this.intent_data.setup ? '/setup_intents/' : '/payment_intents/';
      if (!this.intent_data.setup) {
        params.amount = this.intent_data.amount
        params.currency = this.intent_data.currency
        params.payment_method_options = {
          card: {
          require_cvc_recollection: this.intent_data.require_cvc_recollection
          }
        }
      }

      const {intent} = await this.$axios.$post(url, params)

      this.intent = intent
    },
    mountElement() {
      const element_options = {
        clientSecret: this.intent.client_secret,
        customerSessionClientSecret: this.customer_session.client_secret
      }
      this.elements = this.stripe.elements(element_options)
      this.element = this.elements.create('payment')
      this.element.on('change', (event) => console.log(event))
      this.element.mount('#payment')
    },
    async confirmIntent() {

      const payload = {
        elements: this.elements,
        confirmParams: {
          return_url: `${window.location.origin}/success`
        }
      }
      let error = {}
      if (this.intent_data.setup) {
        const resp = await this.stripe.confirmSetup(payload)
        if (resp.error) {
          error = resp.error
        }
      } else {
        const resp = await this.stripe.confirmPayment(payload)
        if (resp.error){
          error = resp.error
        }
      }
      if (error) {
        console.error(error)
      }
    }
  }
}
</script>

