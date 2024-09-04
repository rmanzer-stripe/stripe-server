<template>
 <div class="pb-4">
  <v-row justify="center">
    <v-col cols="12" sm="12" md="10">
      <p class="text-h3">Deferred Intent Creation </p>
      <v-divider></v-divider>
      <p class="text-h5">Create a Payment Element without first creating and Intent</p>
    </v-col>
  </v-row>
  <v-row justify="center">
    <v-col cols="12" sm="12" md="3">
      <div v-if="stripeObjects.length > 0">
        <p class="text-h4 my-4">Stripe Object Selector</p>
        <v-radio-group v-model="selectedObject">
          <v-radio
          v-for="object in stripeObjects"
          :key="object"
          :label="`${object}`"
          :value="object"
          ></v-radio>
        </v-radio-group>
        <v-bottom-sheet v-model="showObject" inset>
          <template v-slot:activator="{on, attrs}">
            <v-btn class="my-6 white--text" color="teal darken-4" elevation="3" v-bind="attrs" v-on="on">Show Stripe Object</v-btn>
          </template>
          <v-sheet class="" height="">
            <v-row justify="end" class="ma-0 px-2 grey lighten-2" >
              <v-btn icon @click="showObject = !showObject">
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </v-row>
            <stripe-object-view :stripe-object="stripeObject" />
          </v-sheet>
        </v-bottom-sheet>
      </div>
    </v-col>
    <v-col cols="12" sm="12" md="6">
      <v-form>
        <p class="text-h5">Payment Element Options</p>
        <p class="text-h6">Payment Intent</p>
        <v-select v-model="elementOptions.mode" :items="modeOptions" label="Mode"></v-select>
        <v-text-field v-model="elementOptions.amount" type="number" label="Amount" :disabled="elementOptions.mode !== 'payment'"></v-text-field>
        <v-select v-model="elementOptions.currency" :items="currencyOptions" label="Currency"></v-select>
        <v-row>
          <v-col cols="12" sm="9">
            <v-text-field
              v-model="discount"
              type="number"
              label="Amount to Discount"
              ></v-text-field>
          </v-col>
          <v-col cols="12" sm="3">
            <v-btn color="deep-purple accent-4" class="white--text" @click="applyDiscount">
              <v-icon>mdi-currency-usd-off</v-icon>
              Apply Discount
            </v-btn>
          </v-col>
        </v-row>
        <v-select v-model="elementOptions.setupFutureUsage" :items="futureUsageOptions" label="Future Usage"></v-select>
        <v-select v-model="elementOptions.captureMethod" :items="captureMethods" label="Capture Methods"></v-select>
        <v-row>
          <v-col>
            <v-switch v-model="pmCreation" label="Create Payment Method"></v-switch>
          </v-col>
          <v-col>
            <v-switch v-if="elementOptions.mode !== 'subscription' && pmCreation" v-model="pmAttach" label="Attach Payment Method"></v-switch>

          </v-col>
        </v-row>

        <p class="text-h6">Element Layout</p>
        <v-select v-model="layout.type" :items="elementTypeOptions" label="Layout Type"></v-select>
        <v-row justify="space-around">

          <v-switch v-model="layout.defaultCollapsed" label="Default Collapsed"></v-switch>
          <v-switch v-model="layout.radios" label="Radios"></v-switch>
          <v-switch v-model="layout.spacedAccordionItems" label="Spaced Accordion Items"></v-switch>
        </v-row>
        <v-divider class="my-3"></v-divider>
        <v-btn color="primary" @click="mountElement">
          <v-icon>mdi-plus</v-icon>
          Create/Mount Element</v-btn>
      </v-form>
      <v-form v-if="showFCForm" class="my-8">
        <p class="text-h5">Financial Connections Settings</p>
        <v-select
          v-model="elementOptions.paymentMethodOptions.us_bank_account.verification_method"
          :items="us_bank_account_options.verification_methods"
          label="Verification Method"
          ></v-select>
        <v-select
          v-model="elementOptions.paymentMethodOptions.us_bank_account.financial_connections.permissions"
          :items="us_bank_account_options.financial_connections.permissions"
          multiple
          label="Permissions"
          ></v-select>
          <v-btn color="primary" @click="updateElements">Update Elements</v-btn>
      </v-form>
    </v-col>
    <v-col v-if="elementOptions.mode === 'subscription'" cols="12" sm="12" md="3" >
      <v-form>
        <p class="text-h5">Create Customer</p>
        <p class="text-h6">Enter Customer details</p>
        <v-text-field v-model="customer.email" label="Email" placeholder="jane.doe@example.com"></v-text-field>
        <p class="text-h6">Customer Shipping Address</p>
        <div id="address-element"></div>
        <v-divider class="my-4"></v-divider>
        <p class="text-h5">Select Product</p>
        <p class="text-h6">Select a product to subscribe to</p>
        <product-select :products="availableProducts" @price="setPrice($event)" />
        <v-text-field v-model="quantity" type="number" label="Quantity" hint="How much stuff do you want?" persistent-hint class="my-4"></v-text-field>
      </v-form>
    </v-col>
    <v-col cols="12" sm="12" md="8" offset-md="2">
      <form id="payment-form">
        <div id="payment-element">
          <!-- Payment Element rendered here -->
        </div>
        <error-alert v-if="error" :error="error" />
        <v-row v-if="elements !== null" class="my-4" justify="space-around" >
          <!-- <v-btn color="primary" @click="createPM">
            <v-icon>mdi-credit-card</v-icon>
            Create PM
          </v-btn>
          <v-btn class="white--text amber darken-4" @click="createIntent">
            <v-icon>mdi-cash-sync</v-icon>
            Create Intent
          </v-btn> -->
          <v-btn   color="success" @click="submitIntent">
            <v-icon>mdi-currency-usd</v-icon>
            Confirm Intent</v-btn>
        </v-row>
      </form>
    </v-col>
  </v-row>
 </div>
</template>

<script>
import ErrorAlert from '~/components/stripe/ErrorAlert.vue'
import ProductSelect from '~/components/stripe/ProductSelect.vue'
import StripeObjectView from '~/components/stripe/StripeObjectView.vue'
export default {
  components: { ProductSelect, ErrorAlert, StripeObjectView },
  async asyncData({ $axios}){
    const { results } = await $axios.$get('/products/')
    return {products: results}
  },
  data: () => ({
    error: null,
    elementOptions: {
      mode: 'payment',
      amount: 2099,
      currency: 'usd',
      setupFutureUsage: null,
      captureMethod: 'automatic',
      paymentMethodTypes: ['card'],
      paymentMethodOrder: ['card'],
      paymentMethodOptions: {
        us_bank_account: {
          verification_method: 'automatic',
          financial_connections: {
            permissions: ['payment_method']
          }
        }
      }
    },
    discount: 0,
    pmCreation: false,
    pmAttach: false,
    layout: {
        type: 'tabs',
        defaultCollapsed: false,
        radios: false,
        spacedAccordionItems: false,
      },
    modeOptions: ['setup', 'payment', 'subscription'],
    currencyOptions: ['usd', 'cad', 'eur'],
    elementTypeOptions: ['tabs', 'accordion'],
    captureMethods: ['automatic', 'manual'],
    futureUsageOptions: [
      {value: null, text: 'Null'},
      {value: 'off_session', text: 'Off Session'},
      {value: 'on_session', text: 'On Session'}
    ],
    us_bank_account_options: {
      verification_methods: ['automatic', 'instant'],
      financial_connections: {
        permissions: ['payment_method', 'balances', 'ownership', 'transactions']
      }
    },
    elements: null,
    paymentElement: null,
    client_secret: null,
    pmType: null,
    paymentMethod: null,
    customer: {
      name: null,
      email: null,
      address: null,
    },
    stripeCustomer: null,
    intent: null,
    price: null,
    quantity: 0,
    stripeObjects: ['payment_method', 'customer', 'intent'],
    selectedObject: null,
    showObject: false,
    showFCForm: false,
  }),
  computed: {
    availableProducts() {
      const filteredProducts = this.products.filter(x => x.data.default_price !== null )
      return filteredProducts.map(x => x.data)
    },
    stripeObject() {
      if (this.stripeObjects.length === 0) {
          return {}
      } else {
        switch  (this.selectedObject) {
          case 'payment_method':
            return this.paymentMethod

          case 'customer':
            return this.stripeCustomer

          case 'intent':
            return this.paymentIntent

          default:
            return {}

        }

      }
    }
  },
  methods: {
    genElementsOptions(){
      // Deep copy the component elementOptions object
      const options = JSON.parse(JSON.stringify(this.elementOptions));
      if (this.pmCreation) {
        options.paymentMethodCreation = 'manual'
      }
      options.amount = Number(options.amount)
      if (this.elementOptions.mode === 'setup') {
        delete options.amount
      }
      options.appearance = this.appearance
      return options
    },
    mountElement() {
      const options = this.genElementsOptions()
      try {
        this.elements = this.$stripe.elements(options)
      } catch(error) {
        this.error = error
        return
      }
      const paymentElement = this.elements.create('payment', {layout: this.layout})
      paymentElement.on('change', e => {this.setType(e)})
      paymentElement.mount('#payment-element')
      this.paymentElement = paymentElement

      if (this.elementOptions.mode === 'subscription' && document.getElementById('address-element')) {
        const addressElement = this.elements.create('address', {mode: 'shipping'})
        addressElement.mount('#address-element')
      }
    },
    updateElements() {
      const options = this.genElementsOptions()
      this.elements.update(options)
    },
    setType(e) {
      const pmType = e.value.type
      this.pmType = pmType
      if (this.pmType === 'us_bank_account') {
        this.showFCForm = true
      }
    },
    setPrice(e) {
      this.price = e.default_price;
    },
    setAddress(e) {
      this.customer.name = e.value.name
      this.customer.address = e.value.address
    },
    applyDiscount() {
      /**
       * TODO: Revise approach
       * Change input to accept promo code
       * Send both code and current amount to the server for validation
       * Return new amount calculated from the discount associated with the Promo code.
       */
      if (this.elements !== null) {
        const newAmount = this.elementOptions.amount - this.discount
        this.elements.update({amount: newAmount})
      } else {
        this.error = "please wait until the Payment Element is mounted to apply a discount."
      }
    },
    async submitIntent() {
      // Submit the element -
      const submit = await this.submitElement();
      if (!submit) {
          return;
      }
      if (this.pmCreation) {
        const pm = await this.createPM();
        if (!pm) {
            return;
        }
      }
      const intent = await this.createIntent(this.elementOptions.mode)
      if (!intent) {
        return;
      }
      if (this.elementOptions.mode !== 'subscription') {
        const {error} = await this.confirmIntent(intent.client_secret);
        if (error) {
          this.error = error
        }
      } else {
          const successUrl = `${window.location.origin}/success?subscription=${intent.subscription}`
          this.$route.push(successUrl)
        }

    },
    async submitElement() {
      // Submit the element - I _think_ this is where we create the PM
      const {error: submitError} = await this.elements.submit()
      if (submitError) {
        this.error = submitError
        return false;
      }
      return true
    },
    async createPM(){
      if (this.pmCreation && this.pmType !== null) {
        await this.submitElement();
        const {error, paymentMethod} = await this.$stripe.createPaymentMethod({
          elements: this.elements
        })
        if (error) {
          this.error = error
          return false;
        }
        this.paymentMethod = paymentMethod

        return true
      }
    },
    async createCustomer() {
      const payload = {name: this.customer.name, email: this.customer.email}
      if (this.elementOptions.mode === 'subscription' && this.paymentMethod) {
        payload.invoice_settings = {default_payment_method: this.paymentMethod.id}
      }
      try {
        const { customer } = await this.$axios.$post('/customers/', payload)

        return customer
      } catch (error) {
        this.error = error.response
        return false
      }
    },
    async createIntent(mode){
      if (mode !== undefined) {
        let payload = {}
        let url = null
        if (mode === 'payment') {
            payload = {
                    amount: this.elementOptions.amount - this.discount,
                    currency: this.elementOptions.currency,
                    automatic_payment_methods: {enabled: true},
                    capture_method: this.elementOptions.captureMethod,
                  }
              if (this.elementOptions.setupFutureUsage !== null) {
                payload.setup_future_usage = this.elementOptions.setupFutureUsage
              }
              url = '/payment_intents/'
          } else if (mode === 'setup') {
            const customer = await this.createCustomer()
            payload = {
              customer: customer.id,
              automatic_payment_methods: {enabled: true},
              payment_method_options: {card: {request_three_d_secure: true}}
            }
            url = '/setup_intents/'
          } else if (mode === 'subscription') {
            const customer = await this.createCustomer()
            if (!customer) {
              return ;
            }
            payload = {
              customer: customer.id,
              items: [{
                price: this.price,
                quantity: this.quantity
              }]
            }
            url = '/subscriptions/'
          }
          try {
            const {intent, error} = await this.$axios.$post(url, payload)
            if (error) {
              this.error = error
              return
            }

            this.intent = intent
            return intent
          } catch(error) {
            this.error = error.response.data.error
            return false
          }
      }
    },
    async confirmIntent(clientSecret){
      let response = null
      const payload = {
                        elements: this.elements,
                        clientSecret,
                        confirmParams: {
                          return_url: `${window.location.origin}/success`
                        }
                      }
      if (this.elementOptions.mode === 'setup') {
        response = await this.$stripe.confirmSetup(payload)
      } else {
        response = await this.$stripe.confirmPayment(payload)
      }
      this.paymentIntent = response
      return response
    },

  },

}
</script>
