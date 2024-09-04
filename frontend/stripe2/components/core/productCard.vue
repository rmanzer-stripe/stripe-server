<template>
  <v-card
    :color="color"
    min-height="200"
    class="ma-4"
    @click="$emit('click', product.price)"

  >
  <v-row>
    <v-col cols="12" md="4">
      <v-card-title class="text-h5" v-text="product.name"></v-card-title>
      <v-card-subtitle v-text="product.description"></v-card-subtitle>

    </v-col>
    <v-col cols="12" md="8">
      <v-avatar class="ma-2" size="200" tile>
      <v-img :src="product.image_url"></v-img>
    </v-avatar>
    </v-col>
</v-row>
  </v-card>
</template>

<script>
export default {
  model: {
    prop: 'product',
    event: 'click'
  },
  props: {
    product: {
      type: Object,
      required: true
    },
    color: {
      type: String,
      required: false,
      default: "blue-grey lighten-5"
    }
  },
}
</script>
