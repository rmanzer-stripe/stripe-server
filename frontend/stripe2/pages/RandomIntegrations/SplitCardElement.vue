<template>
<v-card>
  <v-img
  src="https://images.pexels.com/photos/4466420/pexels-photo-4466420.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
  gradient="to top, rgba(0,0,0,0.5), rgba(0,0,0,0.1)"
  alt="split cards"
  class="align-end white--text"
  height="300"
  >
    <v-card-title>
      Split Card Element
    </v-card-title>
  </v-img>

  <v-card-text>
    <p class="text-h3">This is where I'll load the Split card element</p>
    <v-row>
      <v-col class="lg-6 md-12">
        <div id="card-num"></div>
      </v-col>
      <v-col class="lg-6 md-12">
        <div id="card-expir"></div>
      </v-col>
      <v-col class="lg-6 md-12">
        <div id="card-cvc"></div>
      </v-col>
    </v-row>
  </v-card-text>
  <v-divider></v-divider>
  <v-card-actions>
    <v-row justify="space-around" class="my-4">
      <v-btn @click="mountCard">Mount Element</v-btn>
    </v-row>
  </v-card-actions>
</v-card>
</template>

<script>
export default {
  data: () => ({
    elements: null,
    cardNumber: null,
    cardExpiry: null,
    cardCvc: null,
    cardOptions: {
      showIcon: true,
    }
  }),
  methods: {
    async mountCard() {
      this.elements = await this.$stripe.elements({
        mode: 'payment',
        currency: 'eur',
        amount: 1499
      })
      this.cardNumber = this.elements.create('cardNumber', this.cardOptions)
      this.cardNumber.mount('#card-num')
      this.cardCvc = this.elements.create('cardCvc')
      this.cardCvc.mount('#card-cvc')
      this.cardExpiry = this.elements.create('cardExpiry')
      this.cardExpiry.mount('#card-expir')
    }
  }
}
</script>

