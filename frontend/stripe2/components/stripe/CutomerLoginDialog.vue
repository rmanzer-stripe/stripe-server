<template>
  <v-dialog
   v-model="customerDialog"
   persistent
   max-width="600px">
   <template v-slot:activator="{on: dialog, attrs}">
     <v-tooltip left>
       <template v-slot:activato="{on: tooltip}">
         <v-btn
          icon
          v-bind="attrs"
          v-on="{...tooltip, ...dialog}"
         >
          <v-icon v-if="!customerLoggedIn">
            mdi-account-alert-outline
          </v-icon>
          <v-icon v-else>
            mdi-account
          </v-icon>
         </v-btn>
       </template>
       <span v-text="iconTooltipText"></span>
     </v-tooltip>
   </template>
   <v-card>
     <v-card-title>Select Customer</v-card-title>
     <v-card-subtitle>This allows the page to treat you as an authenticated customer</v-card-subtitle>
     <v-card-text>
       <v-container>
         <v-row align="center">
           <customer-select />
         </v-row>
       </v-container>
     </v-card-text>
   </v-card>
  </v-dialog>
</template>

<script>
import CustomerSelect from './CustomerSelect.vue'
export default {
  components: { CustomerSelect },
  data: () => ({
    customerDialog: false,
  }),
  computed: {
    customerLoggedIn() {
      return this.$store.state.customer !== null
    },
    iconTooltipText() {
      if (this.customerLoggedIn) {
        return `Logged in as ${this.$store.state.cutomer.name}`
      } else {
        return "Select customer to log in as"
      }
    }
  }
}
</script>

<style>

</style>
