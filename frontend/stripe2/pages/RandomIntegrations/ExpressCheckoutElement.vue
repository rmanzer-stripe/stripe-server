<template>
  <v-row align="center">
    <v-col cols="12" sm="4">
     <v-card>
      <v-img
        src="https://images.pexels.com/photos/1181202/pexels-photo-1181202.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
        height="250"
        gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,0.7)"
        class="align-end white--text"
      >
        <v-card-title>
          Express Checkout Element Options
        </v-card-title>
        <v-divider color="white"></v-divider>
        <v-card-subtitle>
          Select options for ECE component work flow. Once ready click "Mount Element"
        </v-card-subtitle>
      </v-img>
        <v-card-text>
          <v-form :disabled="form_disabled">
            <v-text-field v-model="options.amount" type="number" @change="setInt"></v-text-field>
            <currency-select :default="options.currency" @currency="setCurrency"/>
            <mode-select :default="options.mode" @mode="setMode" />
            <v-row justify="space-around" class="mx-4">
              <v-col>
                <v-switch
                  v-model="request_payer_info"
                  label="Request Payer Info"
                  color="green"
                ></v-switch>
              </v-col>
              <v-col>
                <v-switch
                  v-model="request_shipping"
                  label="Request Shipping"
                  color="indigo"
                ></v-switch>
              </v-col>
              <v-col>
                <v-switch
                  v-model="display_line_items"
                  label="Show Line Items"
                  color="purple"
                ></v-switch>
                <v-switch
                  v-model="collectAddress"
                  label="Collect Address"
                  color="teal lighten-1"
                >
                </v-switch>
              </v-col>
              <v-col>
                <v-switch v-model="create_pm" label="Create PM" color="amber"></v-switch>
              </v-col>
            </v-row>

          </v-form>
        </v-card-text>
     </v-card>
    </v-col>
    <v-col cols="12" sm="6" align="center">
      <div id="address-element">
        <v-card class="indigo" height="300">
          <v-card-title class="white--text">Address Element loaded here</v-card-title>
          <v-divider class="white"></v-divider>
          <v-card-text class="white--text">
            This content will be replaced by the Address Element when mounted
          </v-card-text>
        </v-card>
      </div>
      <div id="express-checkout-element">
        <v-card color="teal lighten-4" height="300">
          <v-card-title>
            Express Checkout Element Loaded Here
          </v-card-title>
          <v-divider></v-divider>
          <v-card-subtitle>
            This will get replaced by the element once you mount it
          </v-card-subtitle>
        </v-card>
      </div>
    </v-col>



        <v-col cols="12" sm="2" justify="end">
          <p class="text-h5">Workflow Steps</p>
          <v-divider></v-divider>
          <v-btn block class="primary my-2" @click="mountExpressCheckout">Mount Element</v-btn>
          <!-- <v-btn block class="primary my-2" @click="createPaymentIntent">Create PI</v-btn> -->

        </v-col>


    <v-col>
      <div id="error-message">
        <error-alert :error="error"></error-alert>
      </div>
    </v-col>
  </v-row>
</template>

<script>
import CurrencySelect from '~/components/stripe/CurrencySelect.vue'
import ErrorAlert from '~/components/stripe/ErrorAlert.vue'
import ModeSelect from '~/components/stripe/ModeSelect.vue'
export default {
  components: { ErrorAlert, CurrencySelect, ModeSelect },
  props: {
    successUrl: {type: String, required: false, default: ""}
  },
  data: () => ({
    elements: null,
    element: null,
    clientSecret: null,
    intent: null,
    error: null,
    options: {
      mode: 'payment',
      amount: 6000,
      currency: 'usd',
    },
    line_items: [
      {name: 'T-shirt', amount: 5000 },
      {name: 'Tax', amount: 1000},
      {name: 'Shipping', amount: 0}
    ],
    loading: false,
    request_payer_info: false,
    request_shipping: false,
    display_line_items: false,
    create_pm: true,
    paymentMethod: null,
    form_disabled: false,
    collectAddress: false,
  }),
  computed: {
    clickOptions(){
      const options = {}
      if (this.request_payer_info) {
        options.emailRequired = true
        options.phoneNumberRequired = true
      }
      if (this.request_shipping) {
        options.shippingAddressRequired = true
      }
      if (this.display_line_items) {
        options.lineItems = this.line_items
      }
      return options
    },
    elOptions() {
      const elsOptions = this.options
      if (this.create_pm) {
        elsOptions.paymentMethodCreation = 'manual'
      }
      return elsOptions
    }
  },
  methods: {
    mountExpressCheckout(){
      if (this.element === null) {

        this.form_disabled = true
        this.elements = this.$stripe.elements(this.elOptions)
        this.element = this.elements.create('expressCheckout')
        this.element.mount('#express-checkout-element')
        if (this.collectAddress) {
          const addEl = this.elements.create('address', {mode: 'billing'})
          addEl.mount('#address-element')
        }

      } else {
        this.error = {message:"Express Checkout element already created"}
      }
      this.element.on('click', (event) => {
        this.onClick(event)
      });
      this.element.on('shippingaddresschange', (event) => {
          this.onAddressChange(event)
      })
      this.element.on('ready', (event) =>{
        this.onReady(event)
      })
      this.element.on('confirm', async (event) => {
        await this.confirmPayment(event)
      } )
    },
    onClick(event) {
      let click_options = {}
      const shipping_options = {
          allowedShippingCountries: ['US', 'CA', 'AU', 'GB'],
          shippingRates: [
            {
              id: 'free-shipping',
              displayName: 'Free shipping',
              amount: 0,
              deliveryEstimate: {
              maximum: {unit: 'day', value: 3},
              minimum: {unit: 'day', value: 1}
              }
            },
          ]
        };
        if (this.clickOptions.shippingAddressRequired) {
          click_options = {...this.clickOptions, ...shipping_options}
        } else {
          click_options = this.clickOptions
        }
        event.resolve(click_options);
    },
    onAddressChange(event) {
        const resolve = event.resolve;
        const address = event.address;
        const payload = {}
        console.log("Shipping address change", event)
        const free_options = {
          mode: 'setup',
          amount: 0,
          currency: 'usd'
        }
        if (address.country === 'AU') {
          this.elements.update(free_options)
        } else {
          this.elements.update(this.options)
        }
        resolve(payload)
    },
    onReady(event) {
      console.log("Ready", event);
      this.loading = false
    },

    async createPaymentIntent() {
      const payload = {
        amount: this.options.amount,
        currency: this.options.currency,
        automatic_payment_methods: {enabled: true},
        account: 'acct_1O83hCB9iVsTMEuJ' // British Manzer
      }
      if (this.paymentMethod) {
        payload.payment_method = this.paymentMethod.id
      }
      const {intent} = await this.$axios.$post('/payment_intents/', payload)
      console.log(intent)
      this.clientSecret = intent.client_secret
      this.intent = intent
      return true
    },
    async createSetupIntent() {
      const si = await this.$axios.$post('/setup_intents/', {
        metadata: {'reason': 'ece integration'}
      })
      console.log(si);
      this.clientSecret = si.client_secret
      this.intent = si
    },
    async createSubscription() {
      const items = [{
        price: 'price_1MYe5BIlCeH6bP8Rq4N9xQGK',
        quantity: 1
      }]
      const customer = 'cus_PudQ0AgWw6Hv5c'
      const sub = await this.$axios.$post('/subscriptions', {
        items,
        customer,
      })
      console.log(sub);
    },
    async createIntent() {
      if (this.options.mode === 'payment') {
        await this.createPaymentIntent()
        return true
      } else if (this.options.mode === 'setup') {
        await this.createSetupIntent()
        return true
      } else {
        this.error = {code: 'missing_intent', message: 'No intent was created'}
        return false
      }
    },
    async confirmPayment(event) {

      const {error: SubmitError} = await this.elements.submit();
      if (SubmitError) {
        this.error = SubmitError
        return
      }

      const {error: confError, confirmationToken} = await this.$stripe.createConfirmationToken({
        elements: this.elements
      })
      console.log(confirmationToken);
      console.log(confError);

      // event.paymentFailed({reason: "invalid_shipping_address"})

      if (this.create_pm) {
        const success = await this.createPM()
        console.log(success);
        if (!success) {
          return
        }
      }
      if (this.clientSecret === null) {
        const success = await this.createPaymentIntent()
        if (!success) {
          return
        }
      }
      console.log(this.intent);
      const {error} = await this.$stripe.confirmPayment({
        clientSecret: this.clientSecret,
        confirmParams: {
          return_url: `${window.location.origin}/success`,
          confirmation_token: confirmationToken.id
        }
      })
      if (error) {
        this.error = error
      }
      console.log("Done!")
    },
    async createPM() {
      const {error, paymentMethod} = await this.$stripe.createPaymentMethod({
        elements: this.elements,
        params: {
          billing_details: {
            name: 'Jenmy Rosen'
          }
        }
      })
      if (error) {
        this.error = error
        return false
      } else {
        this.paymentMethod = paymentMethod
        return true
      }
    },
    setCurrency(currency) {
      console.log(currency);
      this.options.currency = currency
    },
    setMode(mode) {
      console.log(mode);
      this.options.mode = mode
      if (mode === 'setup') {
        this.options.amount = null
      } else if (mode === 'subscription'){
        this.options.amount = 12000
      }
    },
    setInt() {
      this.options.amount = Number(this.options.amount)
    }
  }
}
</script>


