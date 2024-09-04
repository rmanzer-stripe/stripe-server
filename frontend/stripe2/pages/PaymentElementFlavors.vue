<template>
  <v-card>
    <v-img
    class="align-end white--text"
    src="https://images.pexels.com/photos/34577/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
    alt="web payment"
    height="300"
    gradient="to top, rgba(0,0,0,0.4), rgba(0,0,0,0.15)"
    >
    <v-card-title>Payment Element Flavors</v-card-title>
    <v-divider class="white--text white" ></v-divider>
    <v-card-subtitle>The many ways we can use the Payment Element</v-card-subtitle>
  </v-img>
  <v-card-text>
    <!-- Toolbar and tabs component-->
    <v-toolbar class="indigo darken-2" dark>
      <template v-slot:extension>
        <v-tabs v-model="pe_tab" align-with-title>
          <v-tabs-slider color="white"></v-tabs-slider>
          <v-tab
            v-for="flavor in flavors"
            :key="flavor.name"
          > {{ flavor.name }} </v-tab>
        </v-tabs>
      </template>
    </v-toolbar>

    <!-- Actual implementation component-->
    <v-tabs-items v-model="pe_tab">
      <v-tab-item
       v-for="flavor in flavors"
       :key="flavor.name"
      >
        <component :is="flavor.component" class="ma-4"></component>
      </v-tab-item>
    </v-tabs-items>
  </v-card-text>
  </v-card>
</template>

<script>
import SavedPaymentMethodsVue from '~/components/stripe/PaymentElementFlavors/SavedPaymentMethods.vue'
export default {
  components: {SavedPaymentMethodsVue, },
  data: () => ({
    pe_tab: null,
    flavors: [
      {
        name: 'Saved PMs',
        component: "SavedPaymentMethodsVue"
      }
    ]
  })
}
</script>

<style>

</style>
