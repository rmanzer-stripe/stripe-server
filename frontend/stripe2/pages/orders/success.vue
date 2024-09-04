<template>
  <v-row align="center" justify="center">
    <v-card flat>
      <v-img
        class="align-end white--text"
        src="https://images.pexels.com/photos/2645414/pexels-photo-2645414.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
        gradient="to top, rgba(0,0,0,0.5), rgba(0,0,0,0.1)"
      >
        <v-card-title class="text-h1">Order Status</v-card-title>
      </v-img>
      <v-card-text>
        <v-alert :type="alertType" border="left" colored-border elevation="3"  >{{ statusMessage }}</v-alert>
        <line-items v-if="hasOrder" :discounts="order.discounts.data" :line-items="order.line_items.data" />
      </v-card-text>
    </v-card>



  </v-row>
</template>

<script>
import LineItems from '~/components/orders/LineItems.vue'
export default {
  components: { LineItems },
  name: "OrderStatus",
  data: () => ({
    order: null
  }),
  computed: {
    orderId () {
      return Object.keys(this.$route.query).includes('order') ? this.$route.query.order : null
    },
    status() {
      return Object.keys(this.$route.query).includes('redirect_status') ? this.$route.query.redirect_status : null
    },
    succeeded() {
      return Object.keys(this.$route.query).includes('redirect_status') ? this.status === "succeeded" : false
    },
    alertType() {
      return this.succeeded ? "success" : "error"
    },
    statusMessage() {
      return this.succeeded ? `Order ${this.orderId} was proceesed successfully.` : "Something appears to have gone wrong in processing"
    },
    hasOrder() {
      return this.order !== null
    }
  },
   mounted() {
    this.syncLocal()
  },
  methods: {
    async syncLocal() {
      if (this.orderId !== null ) {
        const url = `/orders/${this.orderId}/sync/`
        const result = await this.$axios.$post(url);
        this.order = result.order
      }
    }
  },
}
</script>

<style>

</style>
