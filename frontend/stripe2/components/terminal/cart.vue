<template>
  <v-card flat>
      <v-card-text>
          <v-row v-if="success" align="center" justify="center">
            <p class="text-h5">Thank you for your Order!</p>
            <v-icon x-large color="green" class="my-8">
              md-check-circle
            </v-icon>
            <v-btn @click="okNext">Done</v-btn>
          </v-row>

          <v-list
          v-else
          two-line
          dense

          >

          <v-list-item v-for="item in cart" :key="item.text">
            <v-list-item-content>
              <v-list-item-title>{{ item.text }}</v-list-item-title>
              <v-list-item-subtitle>{{ item.description }}</v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action>
              <v-list-item-action-text>{{ myPrice(item.price) }}</v-list-item-action-text>
              <v-btn icon @click="removeItem(item.text)">
                <v-icon>mdi-close-outline</v-icon>
              </v-btn>
            </v-list-item-action>
          </v-list-item>
          <v-list dense>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>Tax:</v-list-item-title>
              </v-list-item-content>
              <v-list-item-action>
                <v-list-item-action-text>{{ myPrice(tax) }}</v-list-item-action-text>
              </v-list-item-action>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>Total:</v-list-item-title>
              </v-list-item-content>
              <v-list-item-action>
                <v-list-item-action-text>{{ myPrice(total) }}</v-list-item-action-text>
              </v-list-item-action>
            </v-list-item>
          </v-list>
          <v-divider></v-divider>
          <v-list-item >
            <v-list-item-content>
              <v-list-item-title>Clear Cart?</v-list-item-title>
            </v-list-item-content>
            <v-list-item-action>
              <v-btn text color="error" @click="clearCart">
                clear
              </v-btn>
            </v-list-item-action>
          </v-list-item>
          <v-list-item >
            <v-list-item-content>
              <v-list-item-title>Calculate Tax</v-list-item-title>
            </v-list-item-content>
            <v-list-item-action>
              <v-btn text color="green lighten-2" @click="calculateTax">
                calc tax
              </v-btn>
            </v-list-item-action>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>Show Cart?</v-list-item-title>
            </v-list-item-content>
            <v-list-item-action>
              <v-btn text color="teal darken-2" @click="emitDisplay">Display Cart</v-btn>
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
  name: "TerminalCart",
  props: {
    cart: {type: Array, required: false, default: () => []},
    total: {type: Number, required: false, default: 0},
    tax: {type: Number, required: false, default: 0},
    success: {type: Boolean, required: false, default: false}
  },
  methods: {
    emitCheckout() {
      this.$emit('checkout', 'Hi!')
    },
    emitDisplay() {
      this.$emit('display')
    },
    clearCart() {
      this.$emit('clear-cart')
    },
    removeItem(name) {
      this.$emit('remove', name)
    },
    calculateTax() {
      this.$emit('calc-tax')
    },
    myPrice(amount){
      return this.$format.stripePrice(amount)
    },
    okNext() {
      this.$emit('next-order')
    }
  }
}
</script>
