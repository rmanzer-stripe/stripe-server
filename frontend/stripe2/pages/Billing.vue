<template>
  <v-card outlined class="mx-6">
    <v-img
      class="align-end white--text"
      src="https://images.pexels.com/photos/6964105/pexels-photo-6964105.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
      gradient="to top, rgba(0,0,0.3), rgba(0,0,0,0.1)"
      position="bottom center"
      height="300"
      >
      <v-card-title>Stripe Billing</v-card-title>
      <v-divider class="white"></v-divider>
      <v-card-subtitle>Various scenarios about Stripe Billing</v-card-subtitle>
    </v-img>
    <v-card-text class="pa-4 ">
      <v-toolbar
          color="indigo"
          dark
          flat
        >
        <v-toolbar-title>Billing Integrations</v-toolbar-title>
        <v-spacer></v-spacer>
        <template v-slot:extension>
          <v-tabs
          v-model="tab"
          align-with-title>
            <v-tabs-slider color="white"></v-tabs-slider>

            <v-tab
              v-for="item in billing_integrations"
              :key="item.name"
             >
             {{ item.name }}
            </v-tab>
          </v-tabs>
        </template>
      </v-toolbar>

        <v-tabs-items v-model="tab">
          <v-tab-item
            v-for="item in billing_integrations"
            :key="item.name"
          >
            <component :is="item.component" class="mx-4"/>
          </v-tab-item>
        </v-tabs-items>

    </v-card-text>
  </v-card>
</template>

<script>
import BillingEntitlementsVue from '~/components/billing/BillingEntitlements.vue'
import MetersVue from '~/components/billing/Meters.vue'

export default {
  name: 'StripeBilling',
  components: {BillingEntitlementsVue, MetersVue, },
  data: () => ({
    billing_integrations: [
      {
        name: 'Billing Meters',
        component: "MetersVue"
      },
      {
        name: 'Entitlements',
        component: 'BillingEntitlementsVue'
      }
    ],
    tab: null,
    image_src: 'https://images.pexels.com/photos/6964105/pexels-photo-6964105.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'
  })
}
</script>

<style>

</style>
