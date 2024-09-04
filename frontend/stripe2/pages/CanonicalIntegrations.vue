<template>
  <v-row>
    <v-col cols="12" md="10" offset-md="1" sm="12">
      <v-card flat>
        <v-img
        src="/images/stripe2.png"
        height="350"
        contain
        gradient="to bottom, rgba(0,0,0,0.05), rgba(0,0,0,0.25)"
        class="align-end"
        >
            <v-card-title>Canonical Integrations</v-card-title>
            <v-divider></v-divider>
            <v-card-subtitle>Core Stripe integrations designed to provide ready examples - Updated: 3/7/2024</v-card-subtitle>
        </v-img>
        <v-card-text>
          <nuxt-child />
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>

</template>

<script>
export default {
 data: () => ({
  links: [
    {to: {name: 'CanonicalIntegrations-AcceptPayment'}, title: 'Accept a Payment'},
    {to: {name: "CanonicalIntegrations-ConfirmationTokens"}, title: 'Confirmation Tokens'},

  ]
 }),
 mounted() {
    this.$store.commit('setNavLinks', this.links)
  },
}
</script>


