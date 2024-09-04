<template>
  <v-list
    subheader
    two-line
  >
   <v-subheader>Line Items</v-subheader>
   <line-item
    v-for="item in lineItems"
    :key="item.id"
    :line-item="item"
    />
    <v-subheader>Taxes & Discounts</v-subheader>
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title>Total Discounts Applied: {{ stripePrice(totalDiscounts) }}</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title>Total Tax: {{ stripePrice(totalTax) }}</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-subheader>Grand Total</v-subheader>
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title>Total: {{ stripePrice(grandTotal) }}</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
  </v-list>
</template>

<script>
import LineItem from './LineItem.vue'
export default {
  components: { LineItem },
  props: {
    lineItems: {type: Array, required: false, default: () => []},
    discounts: {type: Array, required: false, default: () => []}
  },
  computed: {
    subtotal() {
      return this.lineItems.reduce((p, item) => p + item.amount_subtotal, 0)
    },
    totalDiscounts() {
      return this.lineItems.reduce((p, item) => p + item.amount_discount, 0)
    },
    totalTax() {
      return this.lineItems.reduce((p, item) => p + item.amount_tax, 0)
    },
    grandTotal() {
      return this.lineItems.reduce((p, item) => p + item.amount_total, 0)
    }
  },
  methods: {
    stripePrice(amount) {
      if (amount !== null || amount !== undefined) {
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

<style>

</style>
