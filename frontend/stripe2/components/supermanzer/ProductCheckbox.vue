<template>
  <v-checkbox
    v-model="selected"
    :label="`${price.product.name} - ${priceString}`"
    @change="emitProduct"
  ></v-checkbox>
</template>

<script>
export default {
  props: {
    price: {type: Object, required: false, default: () => {}}
  },
  data: () => ({
    selected: false
  }),
  computed: {
    priceString(){
      if (this.price.type === 'recurring') {

        return `${this.$format.stripePrice(this.price.unit_amount)} per ${this.price.recurring.interval}`
      } else {

        return `${this.$format.stripePrice(this.price.unit_amount)}`
      }
    }
  },
  methods: {
    emitProduct(){
      this.$emit('selected-product', {price: this.price.id, selected: this.selected})
    }
  }
}
</script>
