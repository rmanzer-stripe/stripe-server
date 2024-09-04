<template>
    <v-col cols="12" sm="12" md="8">
      <v-text-field v-model="amount" type="number" label="Amount to Charge" :rules="rules">
        <v-icon slot="append" color="green darken-2"> mdi-currency-usd</v-icon>
      </v-text-field>
    </v-col>
</template>

<script>
export default {
  data: () => ({
    amount: 50,
    rules: [
    value => value >= 50 || '.50 minimum amount'
   ]
  }),
}
</script>
