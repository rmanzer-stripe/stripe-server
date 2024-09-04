<template>
  <v-container fluid>
    <v-row align="center">
      <v-col cols="12" sm="12">
        <v-select
        v-model="choice"
        :items="apis"
        item-text="name"
        item-value="url"
        return-object
        single-line
        label="Select API"
        ></v-select>
     </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    choice: null,
    apis: [
      {name: 'Payment Intents', url: 'payment_intents/'},
      {name: 'Customers', url: 'customers/'},
      {name: 'Charges', url: 'charges/'},
      {name: 'Setup Intents', url: 'setup_intents'},
      {name: 'Products', url: 'products/'},
      {name: 'Prices', url: 'prices'},
      {name: 'Subscritions', url: 'subscritpions'},
    ]
  })
}
</script>

<style>

</style>
