<template>
  <v-select
    v-model="product"
    :items="products"
    item-text="name"
    item-value="default_price"
    :hint="`${product.description}`"
    persistent-hint
    return-object
    @change="emitPrice($event)"
  ></v-select>
</template>

<script>
export default {
  props: {
    products: { type: Array, required: false, default: () => [] }
  },
  data: () => ({
    product: {
      description: null
    }
  }),
  methods: {
    emitPrice(e) {
      this.$emit('price', e)
    }
  }
}
</script>
