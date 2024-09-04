<template>
  <v-form>
    <v-row>
      <v-col cols="12" sm="12">
        <p class="text-h5">Register Domains</p>
      </v-col>
      <v-col cols="12" sm="8">
        <v-text-field v-model="domain_name" label="Domain name" hint="Enter the domain name you wish to register" persistent-hint></v-text-field>
      </v-col>
      <v-col cols="12" sm="4">
        <v-switch
         v-model="enabled"
         :label="`Enabled: ${enabled.toString()}`"
        ></v-switch>
      </v-col>
    </v-row>
    <v-row justify="end" class="mx-8">
      <v-btn color="primary" @click="registerDomain">Register</v-btn>
    </v-row>
  </v-form>
</template>

<script>
export default {
  data: () => ({
    domain_name: "",
    enabled: false,
  }),
  methods: {
    async registerDomain() {
      const payload = {
        domain_name: this.domain_name,
        enabled: this.enabled
      }
      const response = await this.$axios.$post('/payment-domains/', payload);
      console.log(response)
      this.$emit('domain-registered', response)
    }
  }
}
</script>
