<template>
  <v-container fluid>
      <p class="text-h4">Registered Payment Domains</p>

        <v-data-table
          :headers="headers"
          :items="domains"
          class="elevation-1"
        >
          <template v-slot:item.created="{item}">
            {{ convertTs(item.created) }}
          </template>

          <template v-slot:item.enabled="{item}">
            <v-chip
              label
              :color="item.enabled ? 'green' : 'red'"
            >
            {{ item.enabled }}
            </v-chip>
          </template>

          <template #item.actions="{item}">
            <v-simple-checkbox
              v-model="item.enabled"
              @click="updateDomain"
            ></v-simple-checkbox>
          </template>
        </v-data-table>

  </v-container>
</template>

<script>
export default {
  data: () => ({
    domains: [],
    headers: [
      {text: 'Domain', value: 'domain_name'},
      {text: 'Created', value: 'created'},
      {text: 'Enabled', value: 'enabled'},
      {text: 'GooglePay', value: 'google_pay.status'},
      {text: 'Link', value: 'link.status'},
      {text: 'PayPal', value: 'paypal.status'},
      {text: 'ApplePay', value: 'apple_pay.status'},
      {text: 'Livemode', value: "livemode"}
    ]
  }),
  mounted() {
      this.getDomains()
    },
  methods:{
    updateDomain(e){
      console.log(e)
    },
    async getDomains() {
      const {domains} = await this.$axios.$get('/payment-domains/')
      if (domains.data) {
        this.domains = domains.data
      }
    },
    convertTs(timestamp) {
      return this.$format.convertTimestamp(timestamp)
    }
  },
}
</script>

