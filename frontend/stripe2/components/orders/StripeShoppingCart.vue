<template>
  <v-container fluid>
    <v-row align="center" justify="around">
      <v-col cols="12" sm="6" md="4" lg="3">
        <v-card>
          <v-card-title>Select Customer for Order</v-card-title>
          <customer-select :customers="customers" @customerSelected="setCustomer" />
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="8" lg="6">
        <product-set />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import CustomerSelect from '../stripe/CustomerSelect.vue'
import ProductSet from './ProductSet.vue'

export default {
  components: { CustomerSelect, ProductSet,  },
  data: () => ({
    customer: null,
  }),
  methods: {
    setCustomer(id) {
      this.customer = id
    }
  }
}
</script>

<style>

</style>
