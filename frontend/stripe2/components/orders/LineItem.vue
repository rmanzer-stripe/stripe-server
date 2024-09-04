<template>
  <v-list-item>
    <v-list-item-content>
      <v-list-item-title v-text="title"></v-list-item-title>
      <v-list-item-subtitle v-text="subtitle"></v-list-item-subtitle>
    </v-list-item-content>
    <v-list-item-action>
      <v-tooltip left>
        <template v-slot:activator="{on, attrs}">
          <v-btn
            v-bind="attrs"
            text
            color="indigo"

            v-on="on"
          >Refund</v-btn>
        </template>
        <span>Currently refunds are only available through the Dashboard</span>
      </v-tooltip>
    </v-list-item-action>
  </v-list-item>
</template>

<script>
export default {
  props: {
    lineItem: {type: Object, required: true}
  },
  computed: {
    title() {
      return `${this.lineItem.product.name} - Total: ${this.stripePrice(this.lineItem.amount_total)}`
    },
    subtitle() {
      return `Quantity: ${this.lineItem.quantity}, Unit Price: ${this.stripePrice(this.lineItem.price.unit_amount)}`
    }
  },
  methods: {
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
