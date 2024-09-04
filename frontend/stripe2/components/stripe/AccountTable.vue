<!-- eslint-disable vue/v-slot-style -->
<template>
  <div>
  <p class="text-h5">Select Connected Account</p>
  <v-data-table
    v-model="selected_account"
    :headers="headers"
    :items="accounts"
    show-select
    single-select
    :loading="is_loading"
    loading-text="Loading accounts.."
  >
</v-data-table>
</div>
</template>

<script>
export default {
  props: {
    accounts: {type: Array, required: false, default: () => []}
  },
  data: () => ({
    selected_account: [],
    headers: [
      {text: 'ID', value: 'id', align: 'start'},
      {text: 'Account Type', value:'type'},
      {text: 'Country', value: 'country'},
      {text: 'Email', value: 'email'},
      {text: 'Charges Enabled', value: 'charges_enabled'},
      {text: 'Payouts Enabled', value: 'payouts_enabled'}
    ]
  }),
  computed: {
    is_loading() {
      return this.accounts.length === 0
    }
  },
}
</script>
