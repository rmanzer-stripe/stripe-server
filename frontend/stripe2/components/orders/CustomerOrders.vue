<template>
  <v-row justify="center">
    <span class="text-h5" v-text="title"></span>
    <v-expansion-panels accordion>
      <v-expansion-panel v-for="order in orders" :key="order.id">
        <v-expansion-panel-header>Order {{order.data.id}} - Created {{makeDateString(order.data.created)}}</v-expansion-panel-header>
        <v-expansion-panel-content>
          <cart-item :price="order.price" :product="order.product" :quantity="order.quantity" :show-action="false" />
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-row>
</template>

<script>
import CartItem from './CartItem.vue'
export default {
  components: { CartItem },
  props: {
    orders: {type: Array, required: false, default: () => []},
    title: {type: String, required: false, default: ''}
  },
  methods: {
    makeDateString(timestamp) {
      return new Date(timestamp*1000).toLocaleDateString()
    }
  }
}
</script>
