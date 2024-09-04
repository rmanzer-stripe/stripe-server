<template>
  <v-container>
    <v-row>
      <v-col>
        <p class="text-h1">Supermanzer's Magic Beans</p>
        <v-divider class="my-4"></v-divider>
        <p class="text-h3">Gourmet coffee from around the world (but mostly Africa)</p>
      </v-col>
    </v-row>
    <v-row>
      <v-col v-for="product in products" :key="product.id" class="ma-8" cols="12" sm="5">
      <!-- <coffee-product-card
        :product="product" /> -->
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
// import CoffeeProductCard from './CoffeeProductCard.vue'

export default {
  // components: {CoffeeProductCard  },
  data: () => ({
    product_ids: [
      "prod_OASe9yxaKxPdTs",
      "prod_OAShbXcejlLw3N",
      "prod_OASlq6aFpfyMNj"
    ],
    products: []
  }),
  async mounted() {
    await this.getProducts()
  },
  methods: {
    async getProducts() {
      for (const prod of this.product_ids) {
        const product = await this.$axios.$get(`/products/${prod}`)
        this.products.push(product.data)
      }
    }
  }
}
</script>


