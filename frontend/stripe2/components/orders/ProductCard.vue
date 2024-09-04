<template>
  <v-card class="mx-auto" width="300px" >
    <v-img
      :src="productImageUrl"
      class="white--text align-end"
      gradient="to bottom, rgba(0,0,0,.2), rgba(0,0,0,.5)"
      height="200px"
    >
      <v-card-title v-text="product.name" class="text-wrap"></v-card-title>
      <v-card-subtitle>
        <span v-for="(line, i) of productSubtitle.split('\n')" :key="i">
          {{line}} <br/>
        </span>
      </v-card-subtitle>
    </v-img>
    <v-card-actions>
       <v-form >
        <v-text-field
          v-model.number="quantity"
          type="number"
          label="Quantity"
          :rules="quantityRules"
        ></v-text-field>
      </v-form>
      <v-spacer></v-spacer>
      <v-tooltip bottom>
        <template v-slot:activator="{on, attrs}">
        <v-btn icon color="indigo" v-bind="attrs" v-on="on" @click="$emit('productClick', {product, quantity, price})" >
          <v-icon>mdi-plus-thick</v-icon>
        </v-btn>
        </template>
        Add to shopping cart
      </v-tooltip>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {

  props: {
    product: {type: Object, required: true}
  },
  emits: ['productClick'],
  data: () => ({
    quantity: 1,
    quantityRules: [
      v => v > 0 || 'quantity must be greater than 0' ,
      v => v < 6 || 'quantity must be less than 6'
    ],
    price: {}
  }),
  computed: {
    productImageUrl() {
      return this.product.images.length >0 ? this.product.images[0]: 'https://images.pexels.com/photos/911758/pexels-photo-911758.jpeg?cs=srgb&dl=pexels-gdtography-911758.jpg&fm=jpg'
    },
     productSubtitle() {
       if (this.product !== null) {
        return this.product.description !== null && this.product.description.length > 0 ? `${this.product.description}\n${this.stripePrice()}` : this.stripePrice()
       } else {
         return ''
       }
    }
  },
  created() {
    this.getPrice()
  },
  methods: {
    async getPrice() {
      const { results } = await this.$axios.$get(`/prices?search=${this.product.id}`)
      const prices = results.filter((price) => price.recurring == null)
      if (prices.length > 0){
        this.price = prices[0].data
      }
    },
    stripePrice() {
      const float = this.price.unit_amount / 100;
      const fmt = Intl.NumberFormat('en-US', {
            style: "currency",
            currency: "USD",
        });
      return `${fmt.format(float)}`
    },
  }
}
</script>
