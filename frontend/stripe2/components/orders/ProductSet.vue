<template>
  <v-row justify="center">
    <v-col v-for="product in products" :key="product.id" cols="12" sm="12" md="6" lg="4" >
      <product-card :product="product.data" @productClick="addProduct" />
    </v-col>
 </v-row>
</template>

<script>
import ProductCard from './ProductCard.vue'


export default {
  components: { ProductCard },
  props: {
    products: {type: Array, required: true}
  },
  methods: {
    addProduct(productObj) {
      this.$emit('addProduct', productObj)
    }
  }
}
</script>
