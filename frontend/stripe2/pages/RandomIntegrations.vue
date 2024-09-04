<template>
  <v-card flat>
    <!-- <v-app-bar
      color="teal lighten-2"
      dense
      dark
    >

      <v-toolbar-title>{{ toolbarTitle }}</v-toolbar-title>
    </v-app-bar> -->

    <v-card-text>
      <NuxtChild :success_url="successUrl" v-on:update:title="setChildTitle" />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  data: () => ({
    navigation: false,
    group: null,
    title: "Miscellaneous Integrations",
    child_title: null,
    links: [
      {to: {name: 'RandomIntegrations-PaymentAddress'}, title: 'Payment/Address'},
      {to: {name: 'RandomIntegrations-DeferredIntent'}, title:'Deferred Intent'},
      {to: {name: 'RandomIntegrations-DeferredIntentSub'}, title: 'Deferred Intent Subscriptions'},
      {to: {name: 'RandomIntegrations-CardElement'}, title: 'Card Element'},
      {to: {name: 'RandomIntegrations-LinkCheckout'}, title: 'Link Checkout'},
      {to: {name: 'RandomIntegrations-ACHDirectDebit'}, title: 'ACH Direct Debit'},
      {to: {name: 'RandomIntegrations-Checkout'}, title: 'Checkout'},
      {to: {name: 'RandomIntegrations-PricingTable'}, title: 'Pricing Table'},
      {to: {name: 'RandomIntegrations-ExpressCheckoutElement'}, title: 'Express Checkout'},
      {to: {name: 'RandomIntegrations-BankTransfers'}, title: 'Bank Transfer'},
      {to: {name: "RandomIntegrations-EmbeddedCheckout"}, title: "Embedded Checkout"},
      {to: {name: 'RandomIntegrations-ACHConnect'}, title: 'ACH Connect A - B'},
      {to: {name: 'RandomIntegrations-PaymentElement'}, title: 'Payment Element - Plain'},
      {to: {name: 'RandomIntegrations-Affirm'}, title: "Affirm"},
      {to: {name: 'RandomIntegrations-PaymentDomain'}, title: "Payment Domains"},
      {to: {name: 'RandomIntegrations-ConfirmationTokens'}, title: "Confirmation Tokens"},
      {to: {name: 'RandomIntegrations-SavedPM'}, title: "Saved Payment Methods"},
      {to: {name: 'RandomIntegrations-FinancialConnections'}, title:'Financial Connections'},
      {to: {name: 'RandomIntegrations-PaymenrRequest'}, title: 'PRB'},
      {to: {name: 'RandomIntegrations-MessagingElement'}, title: 'Messaging'},
      {to: {name: 'RandomIntegrations-BillingMeter'}, title: "Billing Meter"},
      {to: {name: 'RandomIntegrations-ApplePay'}, title: "Apple Pay"},
      {to: {name: 'RandomIntegrations-RevolutPay'}, title: 'Revolut Pay'},
      {to: {name: 'RandomIntegrations-SplitCardElement'}, title: 'Split Card'}

    ]
  }),
  computed :{
    toolbarTitle() {
      if (this.child_title != null) {
        return `${this.title} - ${this.child_title}`
      } else {
        return this.title
      }
    },
    successUrl() {
      return `${window.location.origin}/success`
    }
  },
  mounted() {
    this.$store.commit('setNavLinks', this.links)
  },
  methods: {
    setChildTitle(e) {
      this.child_title = e
    }
  },
}
</script>

