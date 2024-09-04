<template>
  <v-row class="my-10">
    <v-col>
      <v-form>
        <p class="text-h4">Create Account</p>
        <v-text-field v-model="email" label="Email"></v-text-field>
        <v-select v-model="type" :items="types" label="Account Type"></v-select>
        <v-select v-model="country" :items="countries" label="Account Country"></v-select>
        <v-select v-model="business_type" :items="business_types" label="Business Type"></v-select>
        <v-row justify="space-around">
          <p class="text-h5">Express & Custom Accounts only</p>
          <v-switch v-model="capabilities.card_payments.requested" :label="`Card payments requested: ${capabilities.card_payments.requested.toString()}`"></v-switch>
          <v-switch v-model="capabilities.transfers.requested" :label="`Transfers requested: ${capabilities.transfers.requested.toString()}`"></v-switch>
          <v-switch v-model="capabilities.us_bank_account_ach_payments.requested" :label="`US ACH requested: ${capabilities.us_bank_account_ach_payments.requested.toString()}`"></v-switch>
        </v-row>
      </v-form>
      <v-btn color="teal darken-3 white--text" @click="createAccount">Create Account</v-btn>
    </v-col>
    <v-col>
      <account-table :accounts="accounts" ref="account_table"/>
      <v-btn color="indigo white--text" @click="onboard_selected">Onboard</v-btn>
      <v-btn color="deep purple white--text" @click="set_account">Set Account</v-btn>
    </v-col>
  </v-row>
</template>

<script>
import AccountTable from './AccountTable.vue'
export default {
  components: { AccountTable },
  data: () => ({
    accounts: [],
    types: ['standard', 'express', 'custom'],
    type: null,
    country: 'US',
    countries: ['US', 'CA', 'GB', 'AU', 'NZ', 'SG', 'HK', 'JP'],
    email: null,
    business_type: 'individual',
    business_types: ['individual', 'company', 'non_profit', 'government_entity'],
    metadata: {},
    capabilities: {
      card_payments: {
        requested: false
      },
      transfers: {
        requested: false
      },
      us_bank_account_ach_payments: {
        requested: false
      }
    }
  }),
  mounted() {
    this.getAccounts()
  },
  methods: {
    async getAccounts() {
      const resp = await this.$axios.$get('/connect-accounts/')
      this.accounts = resp.results.map((x) => x.data)
    },
    async createAccount() {
      const payload = {
        type: this.type,
        country: this.country,
        capabilities: this.capabilities,
        business_type: this.business_type
      }
      const {account} = await this.$axios.$post('/connect-accounts/', payload)
      this.accounts.push(account)
    },
    async onboard_selected(){
      const url = `/connect-accounts/${this.$refs.account_table.selected_account[0].id}/onboarding_link/`

      const payload = {
        return_url: window.location.href,
        refresh_url: window.location.href
      }
      const {account_link} = await this.$axios.$post(url, payload)
      window.location.replace(account_link.url)
    },
    set_account(){
      this.$emit('account-select', this.$refs.account_table.selected_account[0])
    }
  }
}
</script>
