<template>
  <div>
     <v-menu v-if="hasProducts" v-model="cartMenu" offset-y :nudge-width="200" :close-on-content-click="false" left>
          <template v-slot:activator="{on,attrs}">
           <v-badge  bordered color="error" overlap :content="itemsCount">
              <v-icon large v-bind="attrs" v-on="on">mdi-cart</v-icon>
            </v-badge>
          </template>
          <!-- <cart-list :selected-items="selectedItems" @removeItem="removeItem" @clearCart="clearCart" @emitCheckout="emitCheckout" /> -->
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
        </v-menu>

        <v-icon v-else large>mdi-cart-outline</v-icon>
  </div>
</template>

<script>
import CartItem from './CartItem.vue'

export default {
  components: {  CartItem },
  props: {
    selectedItems: {type: Array, required: false, default: () => []}
  },
  data: () => ({
    cartMenu: false,
  }),
  computed: {
    hasProducts() {
      return this.selectedItems.length > 0
    },
    itemsCount() {
      return this.selectedItems.length
    }
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
    stripePrice(amount) {
      if (amount) {
        const fmt = Intl.NumberFormat('en-US', {
            style: "currency",
            currency: "USD",
        });
        const float = amount / 100;
        return `${fmt.format(float)}`
      } else {
        return ''
      }
    }
  }
}
</script>
