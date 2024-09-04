<template>
  <v-container>
    <p class="text-h3">Registered Payment Domains</p>
    <v-divider class="my-4"></v-divider>
    <v-row justify="center">
      <v-col cols="12" sm="4">
        <payment-domain-form ref="form" />
      </v-col>
      <v-col cols="12" sm="8">
        <payment-domain-list ref="table" @domain-registered="logRegister"/>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import PaymentDomainForm from '~/components/stripe/PaymentDomainForm.vue'
import PaymentDomainList from '~/components/stripe/PaymentDomainList.vue'
export default {
  components: { PaymentDomainList, PaymentDomainForm },
  methods: {
    logRegister(e) {
      console.log(e);
      this.$refs.table.getDomains()
    }
  }
}
</script>
