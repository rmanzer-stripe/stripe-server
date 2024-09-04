<!-- eslint-disable no-lonely-if
<template>
  <v-container>
    <v-row>
      <account-get-create
       @account-select="setAccount" />
    </v-row>
    <v-row justify="space-around">
      <create-customer @customer-created="setCustomer" ref="customer"/>
      <v-btn class="indigo lighten-1 white--text" @click="createSetup">Create SI</v-btn>
      <v-btn class="orange darken-2 white--text" @click="getPM">Create PM</v-btn>
    </v-row>
  </v-container>
</template>

<script>
import AccountGetCreate from '~/components/stripe/AccountGetCreate.vue'
import CreateCustomer from '~/components/stripe/CreateCustomer.vue'
export default {
  components: { AccountGetCreate, CreateCustomer },
  name: "ACHConnect",

  data: () => ({
    account: null,
    customer: null,
    setup_intent: null,
    payment_method: null,
    error: null,
    pmSuccess: false
  }),
  computed: {
    // customer() {
    //   return this.$refs.customer.customer
    // }
  },
  methods: {
    setAccount(e){
      this.account = e
    },
    setCustomer(e) {
      this.customer = e
    },
    async createSetup() {
      const payload = {
        customer: this.customer.id,
        payment_method_types: ['us_bank_account']
      }
      const setup_intent = await this.$axios.$post('/setup_intents/', payload)
      this.setup_intent = setup_intent
    },
    async getPM(){
      const payload = {
        clientSecret: this.setup_intent.client_secret,
        params: {
          payment_method_type: 'us_bank_account',
          payment_method_data: {
            billing_details: {
              name: this.customer.name,
              email: this.customer.email
            }
          }
        },
        expand: ['payment_method']
      }
      const response = await this.$stripe.collectBankAccountForSetup(payload)
      console.log(response)
      if (error) {
        this.error = error
      }
      if (setupIntent.status === 'requires_confirmation') {
        console.log("Setup Intent requires confirmation", setupIntent);

        const response = await this.$stripe.confirmUsBankAccountSetup(setupIntent.client_secret)
        console.log(response);
      }



      if (error) {
        this.error = error
      } else {
        console.log(setupIntent);
        // eslint-disable-next-line no-lonely-if
        if (setupIntent.status === 'requires_confirmation') {
          // const usedFinancialConnections = typeof setupIntent.payment_method.financial_connections_account === 'string';
          console.log(setupIntent.payment_method.id)


          if (newError) {
            this.error = newError
          } else if (newSI.status === 'succeeded') {
            const payload = {
              connected_account: this.account.id,
              customer: this.customer.id,
              payment_method: this.payment_method.id,
            }
            const acct_url = `/connect-accounts/${this.account.id}/set_external_account/`
            const response = this.$axios.$post(acct_url, payload)
            console.log(response);
          }
        }
        //   if (newError) {
        //     this.error = newError
        //   } else if (newSetupIntent.status === 'succeeded') {
        //     this.payment_method = setupIntent.payment_method
        //     this.pmSuccess = true
        //   }
        // } else {
        //   // We need stuff
        // }
      }
    }
  }
}
</script> -->
