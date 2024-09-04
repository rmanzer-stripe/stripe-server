<template>
  <v-list-item>
    <v-list-item-content>
      <v-list-item-title v-text="product.name"></v-list-item-title>
      <v-list-item-subtitle>Quantity: {{quantity}},  Unit Price: {{price}}  </v-list-item-subtitle>
    </v-list-item-content>
    <v-list-item-action v-if="showAction">
      <v-btn text color="error" @click="removeItem">
        Remove
      </v-btn>
    </v-list-item-action>
  </v-list-item>
</template>

<script>
export default {
  name: 'CartItem',
  props: {
    product: {type: Object, required: true},
    quantity: {type: Number, required: true},
    price: {type: String, required: true},
    showAction: {type: Boolean, required: false, default: true}
  },
  methods: {
    removeItem() {
      this.$emit('removeItem', this.product.id)
    }
  }
}
</script>
