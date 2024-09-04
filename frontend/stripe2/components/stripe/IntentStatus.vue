<template>
  <v-alert></v-alert>
</template>

<script>
export default {
  props: {
    client_secret: {type: String, required: false, default: ''}
  },
  data: () => ({
    intent: null
  }),
  computed: {
    intentFunction() {
      if (this.client_secret.startsWith('pi_')) {
        return this.$stripe.retrievePaymentIntent
      } else if(this.client_secret.startsWith('si_')) {
        return this.$stripe.retrieveSetupIntent
      } else {
        return false
      }
    }
  },
  methods: {
    async fetchIntent() {
      if (this.intentFunction) {
        this.intent = await this.intentFunction(this.client_secret)
      }
    }
  }
}
</script>

<style>

</style>
