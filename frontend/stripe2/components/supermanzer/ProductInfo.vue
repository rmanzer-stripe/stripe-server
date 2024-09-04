<template>
  <v-card>
    <v-list-item three-line>
      <v-list-item-content>
        <div class="text-overline mb-4">
          PRODUCT
        </div>
        <v-list-item-title>
          {{ product_name }}
        </v-list-item-title>
        <v-list-item-avatar v-if="product_image" tile size="80">
          <v-img :src="product_image"></v-img>
        </v-list-item-avatar>
      </v-list-item-content>
    </v-list-item>
    <v-divider></v-divider>
    <v-card-text>
      <div class="text--h5" v-if="product_description">
        {{ product_description }}
      </div>
      <v-list v-if="product_features">
        <p class="text--primary">Features</p>
        <ul>
          
        </ul>
        <v-list-item-content v-for="feature in product_features" :key="feature">
          <v-list-item-title>{{ feature }}</v-list-item-title>
        </v-list-item-content>
      </v-list>

    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    price: {type: Object, required: false, default: () => {}}
  },
  computed: {
    product_name() {
      if (this.price && this.price.product) {
        return this.price.product.name
      } else {
        return "No product attached"
      }
    },
    product_description() {
      if (this.price && this.price.product) {
        return this.price.product.description
      } else {
        return false
      }
    },
    product_image() {
      if (this.price && this.price.product && this.price.product.inages) {
        return this.price.product.images[0]
      } else {
        return false
      }
    },
    product_features() {
      if (this.price && this.price.product && this.price.product.features) {
        return this.price.product.features.map(x => x.name)
      } else {
        return false
      }
    }
  }
}
</script>

<style>

</style>
