<template>
  <v-container>
    <v-row>
      <v-col>
        <p class="text-h3">Welcome to Big Kahuna Burger - A Hawaiian burger joint</p>
      </v-col>
    </v-row>
    <error-alert :error="error" />
    <v-divider class="my-4"></v-divider>
    <v-row>
      <v-col cols="12" sm="8">
        <p class="text-h6">Create Customer Order</p>
        <v-form>
          <v-select
            v-model="selectedProduct"
            :items="products"
            return-object
            label="Select product"
            :hint="`${selectedProduct.text}, ${selectedProduct.description} - ${stripePrice(selectedProduct.price)}`"
            persistent-hint
            class="my-3"
            ></v-select>
          <v-btn color="teal lighten-4" @click="addToOrder">Add to Order</v-btn>
          <v-divider class="my-4"></v-divider>
          <p class="text-h6">Configure Tipping</p>
          <v-radio-group v-model="tipType" row>
            <v-radio
              label="Percentages"
              value="percentages"
            ></v-radio>
            <v-radio
              label="Fixed Amounts"
              value="fixed_amounts"
            ></v-radio>
          </v-radio-group>
          <v-row justify="space-between" align="baseline">
            <v-col v-for="value, index in tipValues" :key="index" cols="12" sm="2" class="mx-4">
              <v-text-field v-model="tipValues[index]" outlined type="number"></v-text-field>
            </v-col>
            <v-btn color="success" icon :disabled="tipValues.length >= 3" @click="addTipOption" >
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </v-row>
          <v-row align="baseline" justify="space-around">
            <v-btn color="deep-purple" class="white--text" @click="setTipConfig">Add Tip Config</v-btn>
            <v-btn color="grey lighten-2" class="white--text" @click="cancelOrder">Cancel Order</v-btn>
          </v-row>
          <v-row align="baseline" justify="space-around" class="my-4">
            <v-alert :value="tipSuccess" type="success" elevation="2" border="left" colored-border icon="mdi-check-circle" dismissible>
              Tipping configuration set!
            </v-alert>
          </v-row>
        </v-form>

      </v-col>
      <v-col>
        <cart
         v-if="cart.length > 0"
         :cart="cart"
         :tax="cartTax"
         :total="cartTotal"
         :success="orderSuccess"
         @checkout="Checkout"
         @remove="RemoveProduct"
         @clear-cart="clearCart"
         @calc-tax="calculateTax"
         @display="showCart"
         @next-order="reset"
         />
         <v-alert :value="paySuccess" type="success" elevation="2" border="left" colored-border icon="mdi-check-circle" dismissible>
          Please use the card reader to pay the check
        </v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ErrorAlert from '../stripe/ErrorAlert.vue'
import cart from './cart.vue'


export default {
  components: { cart, ErrorAlert },
    props: {
      reader: {type: Object, required: false, default: () => {}}
    },
    data: () => ({
    products: [
     {value:  1, text: "Beer", description: "A tasty beverage", price: 699},
     {value: 2, text: "Burger", description: "This is a tasty burger", price: 1899},
     {value: 3, text: "Coffee", description: "Be cool honey bunny", price: 499},
     {value: 4, text: "Slice of Pie", description: "Strawberry rhubarb", price: 899}
    ],
    selectedProduct: {value:  1, text: "Beer", description: "A tasty beverage", price: 699},
    cart: [],
    tipValues: [15, 0, 0],
    tipType: 'percentages',
    paySuccess: false,
    tipSuccess: false,
    error: null,
    taxRate: 0.085,
    paymentIntent: null,
    orderSuccess: false,
    cartTax: 0,
    taxCalculation: null,
    taxTransaction: null,
    currency: 'usd'
  }),
  computed: {

    cartTotal() {
      return parseInt(this.cart.reduce((pSum, a) => pSum + a.price, 0) + this.cartTax)
    },
    tipConfig() {
      const values = this.tipValues.map((v) => Number(v))
      return {
          usd: {
            [this.tipType]: values
        }
      }
    },
    cartDisplay() {
      const lineItems = this.cart.map(v => ({description: v.text, amount: v.price, quantity: 1}))
      return {
        line_items: lineItems,
        currency: 'usd',
        tax: this.cartTax,
        total: this.cartTotal
      }
    }
  },
  methods: {
    addToOrder() {
      this.cart.push(this.selectedProduct)
    },
    addTipOption() {
      if (this.tipValues.length < 3) {
        this.tipValues.push(0)
      }
    },
    async showCart() {
      if (this.reader) {
        const url = `/terminals/${this.reader.id}/show_cart/`
        try {
          if (this.taxCalculation === null) {
            await this.calculateTax()
          }
          const resp = await this.$axios.$post(url, {cart: this.cartDisplay})
          console.log(resp);
        } catch (error) {
          this.error = error.response.data.error
        }
      }
    },
    async calculateTax() {
      if (this.reader !== null) {
          const line_items = this.cart.map((x) => {
            return {amount: x.price, reference: x.text, tax_behavior: 'exclusive'}
          })
          const payload = {
            customer_details: {
              address: this.reader.location.address,
              address_source: "billing"
            },
            line_items,
            currency: this.currency
          }
          console.log(payload);
          const {tax_calculation} = await this.$axios.$post("/tax_calculations/", payload)
          this.taxCalculation = tax_calculation
          this.cartTax = tax_calculation.tax_amount_exclusive
      } else {
        this.error = {code: 'no_terminal_reader', type:'invalid_request_error', message: 'No reader selected.  Please select a reader first'}
      }
    },
    async createTransaction() {
      if (this.paymentIntent === null || this.taxCalculation === null) {
        this.error = {code: 'missing_parameter', message: "Both payment intent and tax calculation are required to create a tax transaction"}
        return;
      }
      const payload = {
        calculation: this.taxCalculation.id,
        reference: this.paymentIntent.id,
        expand: ['line_items']
      }
      console.log(payload)
      const url = `/tax_calculations/${this.taxCalculation.id}/create_transaction/`
      const {transaction} = await this.$axios.$post(url, payload)
      this.taxTransaction = transaction
    },
    async updateIntentWithTransaction() {
      if (this.paymentIntent !== null && this.taxTransaction !== null) {
        const payload = {
          metadata: {
            'tax_transaction': this.taxTransaction.id
          }
        }
        const url = `/payment_intents/${this.paymentIntent.id}/update_intent/`
        const { intent } = await this.$axios.$post(url, payload)
        this.paymentIntent = intent
      } else {

        this.error = {code: 'missing_parameters', message: 'You are missing either a Payment Intent or Tax Transaction. Both are required for this function.'}
      }
    },
    async getPaymentIntent() {
      this.fetchIntentLoading = true;
      const payload = {
        // capture_method: 'manual',
        payment_method_types: [ 'card_present'],
        currency: 'usd',
        amount: this.cartTotal,
        setup_future_usage: "off_session"
      }
      try {
        const {intent} = await this.$axios.$post('/payment_intents/', payload);
        this.paymentIntent = intent
        console.log(intent);
      } catch (error) {
        this.error = error.response.data.error
      }
    },
    async processPaymentIntent() {
      console.log("processing payment intent", this);
      if (this.paymentIntent) {

        const url = `/terminals/${this.reader.id}/process_intent/`
        const payload = {
          payment_intent: this.paymentIntent.id,
          process_config: {
            tipping: {amount_eligible: this.cartTotal - this.cartTax}
          }
        }
        console.log("Processing Intent", payload, url);
        await this.$axios.$post(url, payload)
      } else {
        this.message = "You're going to need a Payment Intent first.  Try fetching one"
      }
    },
    async captureIntent() {
      const params = {amount_to_capture: this.cartTotal, capture: true}
      const { msg } = await this.$axios.$post(
        `/payment_intents/${this.paymentIntent.id}/capture/`, params
        )
        this.message = msg
    },
    async Checkout() {
      console.log("checkout starting");
      try {
        if (this.taxCalculation === null) {
          console.log("calculating tax");
          await this.calculateTax()
        }
        console.log("retrieving payment intent");
        await this.getPaymentIntent()
        console.log("creating tax transaction");
        await this.createTransaction()
        console.log("updating intent with tax transaction");
        await this.updateIntentWithTransaction()
        console.log("processing intent");
        await this.processPaymentIntent()
        console.log("payment successful");
        await this.captureIntent()
        this.orderSuccess = true
        this.clearCart()
      } catch (error) {
        console.log(error)
        this.error = error.response.data.error
      }
    },
    async cancelOrder(){
      try {
        const url = `/terminals/${this.reader.id}/cancel_action/`
        await this.$axios.$post(url)
        if (this.paymentIntent) {
          const piUrl = `/payment_intents/${this.paymentIntent.id}/cancel/`
          await this.$axios.$post(piUrl)
        }
        this.clearCart()
      } catch (error) {
        this.error = error.request.data.error
      }
    },
    async setTipConfig() {
      try {
        const resp = await this.$axios.$post('/terminals/configure_tips/', {tipping:this.tipConfig})
        console.log(resp);
        this.tipSuccess = true
      } catch (error) {
        this.error = error.response.data.error
      }
    },
    RemoveProduct(text){
      this.cart = this.cart.filter((product) => {return product.text !== text})
    },
    clearCart() {
      this.cart = []
      this.cartTax = 0
      this.paymentIntent = null
      this.taxCalculation = null
      this.taxTransaction = null
    },
    stripePrice(amount) {
      return this.$format.stripePrice(amount)
    },
    reset(){
      this.cancelOrder()
      this.orderSuccess = false
    }
  }
}
</script>

