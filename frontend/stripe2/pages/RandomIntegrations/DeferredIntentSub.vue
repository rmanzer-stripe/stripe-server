<template>
  <div class="py-4 px-8">
    <p class="text-h4">Deferred Intent Subscription Flow</p>
    <p class="text-h5">Select a Product/Price</p>
    <price-select :prices="prices" @price="price = $event" class="my-2"/>
    <p class="text-h5 mt-10">Provide Customer address for tax purposes</p>
    <div id="address-element" class="my-2"></div>
    <p class="text-h5 mt-10">Provide Payment Method Info</p>
    <div id="payment-element" class="my-2"></div>
    <ErrorAlert :error="error" class="mt-5"/>
    <v-row class="mt-8" justify="space-around">
      <v-btn></v-btn>
      <v-btn></v-btn>
      <v-btn></v-btn>
    </v-row>
  </div>
</template>

<script>
import ErrorAlert from '~/components/stripe/ErrorAlert.vue';
import PriceSelect from '~/components/stripe/PriceSelect.vue';
export default {
    components: { ErrorAlert, PriceSelect },
    data: () => ({
      options: {
        mode: 'subscription',
        amount: 2199,
        currency: 'usd'
      },
      elements:  null,
      paymentElement: null,
      addressElement: null,
      error: null,
      prices: []
    }),
    created() {
      this.createElements()
      this.getPrices()
    },
    mounted() {
      this.mountElements()
    },
    methods: {
      async getPrices(){
        this.prices = await this.$axios.$get('/prices/recurring');
        this.prices = this.prices.map(x => x.data)
      },
      createElements() {
        this.elements = this.$stripe.elements(this.options);
        this.paymentElement = this.elements.create('payment')
        this.addressElement = this.elements.create('address', {mode: 'billing'})
      },
      mountElements(){
        if (this.paymentElement != null && this.addressElement != null ) {
          this.paymentElement.mount('#payment-element')
          this.addressElement.mount('#address-element')
        }
      }
    },
}
</script>

<style>

</style>
