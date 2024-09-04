<template>
  <v-card>
    <v-img
    height="350px"
    :src="productImage"
    class="white--text align-end"
    gradient="to top, rgba(0,0,0,.65), rgba(0,0,0,.15)"
    >
    <v-card-title>{{ product.name }}</v-card-title>
  </v-img>
  <v-card-text>
    <v-row align="center">
      <v-col cols="12" sm="12">
        <v-card-subtitle class="text-h6">{{ product.description }}</v-card-subtitle>
      </v-col>
    </v-row>
  </v-card-text>
  <v-card-actions>
    <v-btn class="primary">Subscribe</v-btn>
  </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: {
    product: {type: Object, required: false, default: () => {}}
  },
  data: () => ({
    price: null
  }),
  computed: {
    productImage() {
      return this.product.images[0]
    }
  },
  methods: {
    async getPrice(){
      const url = `/products/${this.product.id}/default_price`
      this.price = await this.$axios.$get(url)
    }
  }
}
</script>

