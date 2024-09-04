<template>
  <v-card>
    <v-row justify="center">
      <v-card-title class="test-h2">Revolut Pay</v-card-title>
    </v-row>
    <v-divider></v-divider>
    <v-card-subtitle>Using the account for British Manzer</v-card-subtitle>
    <v-card-text>
      <div id="pe"></div>
    </v-card-text>
    <v-card-actions>
      <v-btn primary @click="createIntent">Create Setup Intent</v-btn>
      <v-btn class="deep-purple white--text" :disabled="intent === null" @click="confirmSetup">Confirm RP Setup</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  data: () => ({
    intent: null,
    elements: null,
    element: null,
    intentPayload: {
        account: 'acct_1O83hCB9iVsTMEuJ',
        currency: 'usd',
        payment_method_types: ['revolut_pay'],
        payment_method_data: {type: 'revolut_pay'},
        usage: 'off_session',
        customer: 'cus_Ovvpg6fPecDymK'
      }
  }),
  created() {
    // Setting this API key for British Manzer account
    this.$stripe._apiKey = 'pk_test_51O83hCB9iVsTMEuJAZG1sXHvTEocuvmdoy1i6cRTEBpHPuNkgnr6PS0Dgn5QceFfmqfbxgwvJdSyxj80TfiLcSbN00rFGUFO04'
  },
  methods: {
    async createElements() {
      this.elements = await this.$stripe.elements({
        mode: 'setup',
        currency: 'gbp',
        setupFutureUsage: 'off_session'
      })
    },
    async createElement() {
      this.element = await this.elements.create('payment')
      this.element.mount('#pe')
    },
    async createIntent(){
      const {intent} = await this.$axios.$post('/setup_intents/', this.intentPayload)
      this.intent = intent
    },
    async confirmSetup() {
      const {error} = await this.$stripe.confirmRevolutPaySetup(
        this.intent.client_secret,
        {
          return_url: `${window.location.host}/success`,
          mandate_data: {
            customer_acceptance: {
              type: 'online',
              online: {
                infer_from_client: true
              }
            }
          }
        }
      )
      console.log(error);
    }
  }
}
</script>

