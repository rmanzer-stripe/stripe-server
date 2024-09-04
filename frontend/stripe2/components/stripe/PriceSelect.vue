<template>
  <v-select
    v-model="price"
    :items="prices"
    item-text="product.name"
    item-value="default_price"
    :hint="`${productDescription}`"
    persistent-hint
    return-object
    @change="emitPrice($event)"
  ></v-select>
</template>

<script>
export default {
  props: {
    prices: { type: Array, required: false, default: () => [] }
  },
  data: () => ({
    price: {
      description: null
    }
  }),
  computed: {
    productDescription() {
      if (this.price.product != null) {
        return this.price.product.description
      } else {
        return ""
      }
    },

  },
  mounted() {
    if (this.prices.length > 0) {
      this.expandProduct()
    }
  },
  methods: {
    emitPrice(e) {
      this.$emit('price', e)
    },
    expandProduct(){
      this.prices.forEach(async (price) => {
        const product = await this.$axios.$get(`products/${price.product}`)
        price.product = product.data
      })
    }
  }
}
</script>
