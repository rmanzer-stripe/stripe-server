<template>
  <v-row>
    <v-select
    v-model="selectedCustomer"
    :hint="`${selectedCustomer.name} - ${selectedCustomer.email}`"
    :items="customers"
    item-text="name"
    item-value="id"

    return-object
    single-line
    label="Select Customer"
    @input="emitCustomer"
    />
  </v-row>
</template>

<script>
export default {
  data: () => ({
    customers: [],
    selectedCustomer: {
      data: {
        email: '',
        name: ''
      },
    },
  }),
  computed: {
    hasDefaultPM() {
      return Object.keys(this.selectedCustomer).includes('id') ?
        this.selectedCustomer.data.default_source !== null || this.selectedCustomer.data.invoice_settings.default_payment_method !== null
        : true
    }
  },
  mounted() {
    this.fetchCustomers();
  },
  methods: {
    async fetchCustomers() {
      const { customers } = await this.$axios.$get('/customers/')
      const cust_array = customers.data
      this.customers = cust_array.filter((c) => Object.keys(c).includes('name') && c.name !== null && c.email !== null)

    },
    emitCustomer() {
      console.log('Customer emitted');
      this.$emit("customer-selected", this.selectedCustomer )
    }
  }
}
</script>

