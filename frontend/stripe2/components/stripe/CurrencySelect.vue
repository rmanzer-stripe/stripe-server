<template>
  <v-select
    v-model="currency"
    :items="currencies"
    item-text="text"
    item-value="value"
    label="Select currency"
    @change="emitCurrency"
  ></v-select>
</template>

<script>
export default {
  props: {
    currencies: {type: Array, required: false, default: () => [{text: 'USD', value: 'usd'}, {text: 'CAD', value: 'cad'}, {text: 'EUR', value: 'eur'}]},
    default: {type: String, required: false, default: 'usd'}
  },
  data: () => ({
    currency: null,
  }),
  created() {
    this.currency = this.default
  },
  methods: {
    emitCurrency() {
      this.$emit('currency', this.currency)
    }
  }
}
</script>
