/* eslint-disable camelcase */
<template>
  <v-container>
    <v-row justify="center" align="center" class="grey lighten-3">
      <p class="text-h4" v-text="title"></p>
    </v-row>
    <v-row justify="center" >
      <v-col cols="12" sm="6" md="4" lg="3">
        <p class="text-h5">Select Customer for Order</p>
        <customer-select ref="cust_select" class="mr-4"  @customerSelected="setCustomer" />
        <add-list-code ref="promos" />
        <customer-orders :orders="openOrders" />
      </v-col>
      <v-col cols="12" sm="12" md="8" lg="6">

          <v-col cols="12" sm="12" class="d-flex justify-space-between">
            <span class="text-h5">Select 1 or more Products</span>
            <shopping-cart :selected-items="selected_products" @emptyCart="emptyCart" @removeItem="removeItem" @checkout="collectPayment"/>
          </v-col>
        <product-set :products="products" @addProduct="addProduct" />

      </v-col>
      <v-col cols="12" md="4" lg="3">
        <order-payment v-if="hasOrder" :client-secret="clientSecret" :items="selected_products"/>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import CustomerSelect from '../stripe/CustomerSelect.vue'
import AddListCode from '../promos/AddListCode.vue'
import CustomerOrders from './CustomerOrders.vue'
import OrderPayment from './OrderPayment.vue'
import ProductSet from './ProductSet.vue'

import ShoppingCart from './ShoppingCart.vue'

export default {
  components: {  ShoppingCart, ProductSet, OrderPayment, CustomerSelect, CustomerOrders, AddListCode },
  data: ()=>({
    products: [],
    title: 'Orders [beta]',
    selected_products: [],
    currency: 'usd',
    payment: {
      settings: {
        payment_method_types: ['card']
      }
    },
    orderId: null,
    clientSecret: null,
    loading: false,
    customer: null,
    orderSaved: false,
    openOrders: []
  }),
  async fetch() {
    const { results } = await this.$axios.$get('/products/')
    this.products = results
  },
  computed: {
    hasProducts() {
      return this.selected_products.length > 0
    },
    hasOrder() {
      return this.orderId !== null
    },
    hasSecret() {
      // return false
      return this.clientSecret !== null
    }
  },
  methods: {
    setCustomer(customerId) {
      this.customer = customerId
      this.checkOpenOrders(customerId)
    },
    addProduct(productId) {
      this.selected_products.push(productId)
    },
    emptyCart() {
      this.selected_products = []
    },
    removeItem(id) {
      this.selected_products = this.selected_products.filter((obj) => obj.product.id !== id)
    },
    getDiscounts() {
      const promoCodes = this.$refs.promos.applied_codes
      return promoCodes.map((c) => {return {promotion_code: c}})
    },
    async checkOpenOrders(customerId) {
      const params = {'customer': customerId, 'status': 'open'}
      const {results} = await this.$axios.$get('/orders/', {params})
      this.openOrders = results
    },
    makeLineItem(obj) {
      return {product: obj.product.id, quantity: Number(obj.quantity)}
    },
    async placeOrder() {
      const lineItems = this.selected_products.map(this.makeLineItem)
      const discounts = this.getDiscounts()
      const params = {
        currency: this.currency,
        line_items: lineItems,
        payment: this.payment,
        discounts
      }
      if (this.customer !== null) {
        params.customer = this.customer
      }
      const response = await this.$axios.$post('/orders/', params)
      this.clientSecret = response.client_secret
      this.orderId = response.order_id
    },
    collectPayment() {
      this.loading = true
      this.placeOrder()
    }
  }
}
</script>
