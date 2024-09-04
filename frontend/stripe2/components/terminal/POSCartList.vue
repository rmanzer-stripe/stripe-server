<template>
  <v-card>
     <v-card-text>
     <v-list
     two-line
     dense
     >
       <!-- <cart-item
         v-for="item in cart"
         :key="item.name"
         :product="item.product"
         :quantity="item.quantity"
         :price="stripePrice(item.price.unit_amount)"
         @removeItem="removeItem"
         /> -->
      <v-list-item v-for="item in cart" :key="item.name">
        <v-list-item-content>
          <v-list-item-title>{{ item.name }}</v-list-item-title>
          <v-list-item-subtitle>{{ item.description }}</v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-action>
          <v-list-item-action-text>{{ stripePrice(item.price) }}</v-list-item-action-text>
          <v-btn icon @click="removeItem(item.name)">
            <v-icon>mdi-close-outline</v-icon>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
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
export default {
  name:"POSCartList",
  props: {
    cart: {type: Array, required: false, default: () => []}
  },
  methods: {
    emitCheckout() {
      this.$emit('checkout')
    },
    clearCart() {
      this.$emit('clearCart')
    }
  }
}
</script>
