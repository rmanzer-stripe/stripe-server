<template>
   <v-card>
      <v-card-text>
      <v-list
      two-line
      dense
      >
        <cart-item
          v-for="item in selectedItems"
          :key="item.product.id"
          :product="item.product"
          :quantity="item.quantity"
          :price="stripePrice(item.price.unit_amount)"
          @removeItem="removeItem"
          />
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>Clear Cart?</v-list-item-title>
          </v-list-item-content>
          <v-list-item-action>
            <v-btn text color="error" @click="clearCart">
              clear
            </v-btn>
          </v-list-item-action>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
          <v-list-item-title>Proceed to Checkout?</v-list-item-title>
          </v-list-item-content>
          <v-list-item-action>
            <v-btn text color="indigo darken-2" @click="emitCheckout">Checkout</v-btn>
          </v-list-item-action>
        </v-list-item>
      </v-list>
      </v-card-text>
    </v-card>
</template>

<script>
import CartItem from './CartItem.vue'

export default {
  components: {CartItem},
  props: {
    selectedItems: {type: Array, required: true}
  },
  methods: {
  clearCart() {
      this.$emit('emptyCart')
    },
    emitCheckout() {
      this.$emit('checkout')
    },
    removeItem(id) {
      this.$emit('removeItem', id)
    },
    // stripePrice(amount) {
    //   if (amount) {
    //     const float = amount / 100;
    //     return `$${float.toFixed(2)}`
    //   } else {
    //     return ''
    //   }
    // }
  }
}
</script>
