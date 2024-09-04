<template>
  <div>
    <v-row justify="center" class="">
      <v-col cols="12" sm="8" offset-sm="2">
        <p class="text-h4">Payment + Address Elements</p>
        <v-divider></v-divider>
        <p class="text-h6">Collecting Customer info with Elements</p>
      </v-col>
    </v-row >
      <v-row class="pa-5">
        <v-col cols="12" sm="12" md="4">
          <v-form class="ma-4">
            <v-row>
              <v-col cols="12" sm="12" md="6">
                <v-text-field v-model="amount" :rules="amountRules" type="number" label="Amount to Charge" :disabled="mode === 'setup'"></v-text-field>
              </v-col>
              <v-col cols="12" sm="12" md="6">
                <v-text-field v-model="currency" label="Currency" readonly ></v-text-field>
              </v-col>
              <v-col cols="12" sm="12" md="6">
                <v-select v-model="mode" :items="modes" label="Select Payment Mode"></v-select>
              </v-col>
              <v-col cols="12" sm="12" md="6">
                <v-switch v-model="collect_address" :label="`Collect address: ${collect_address}`"></v-switch>
              </v-col>
              <v-col cols="12" sm="12" md="6">
                <v-select v-model="addressOptions.mode" :items="addressModes" label="Select Address Mode" :disabled="!collect_address"></v-select>
              </v-col>
              <v-col cols="12" sm="12" md="4" offset-md="6">
                <v-btn color="primary" :disabled="hasPi" @click="generateIntent">Generate Intent</v-btn>
              </v-col>
            </v-row>
          </v-form>
        </v-col>
        <v-col cols="12" sm="12" md="6">
          <v-alert v-if="error" type="error" border="left" colored-border elevation="2">
            <pre>{{ error }}</pre>
          </v-alert>
          <div v-show="clientSecret">
            <div id="express-checkout"></div>
            <div id="payment-element"></div>
            <div id="address-element" v-if="collect_address"></div>
            <v-divider class="my-8"></v-divider>
            <v-btn color="primary" @click="confirmIntent">Confirm Intent</v-btn>
          </div>
          <div v-show="!clientSecret">
            <v-alert type="info" border="left" colored-border elevation="1">
              Payment and Address Elements will be loaded here once the server returns a Payment Intent <pre>client_secret</pre>
            </v-alert>
          </div>
        </v-col>
      </v-row>
  </div>
</template>

<script>
export default {
  name: 'PaymentAddress',
  data: () => ({
    amount: 50,
    currency: 'USD',
    amountRules: [
      v => v > 50 || "Minimum amount value is 50",
      v => v < 99999999 || 'Maximum amount value is 99999999'
    ],
    clientSecret: null,
    error: null,
    elements: null,
    mode: 'payment',
    modes: ['payment', 'setup'],
    addressModes: ['shipping', 'billing'],
    collect_address: true,
    paymentOptions: {
      layout: {
        type: 'accordion',
        defaultCollapsed: true
      },
      // defaultValues:{
      //   billingDetails: {
      //     name: "Rudolpho Numbat",
      //     email: "ruddy.numbat@bufo.io"
      //   }
      // },
      fields: {
        name: 'never'
      }
      // paymentMethodOrder: ['apple_pay',  ]
    },
    paymentElement: null,
    addressElement: null,
    addressOptions: {
      mode: 'shipping',
    //   contacts: [
    // {
    //   "name": "edgar",
    //   "address": {
    //     // "line1": "14519 Sherman Way",
    //     "city": "Los Angelesn",
    //     "state": "CA",
    //     "postal_code": "91405",
    //     "country": "US"
    //   },
    //   "phone": "+19166734562"
    // },
    //   {
    //     "name": "Santiago",
    //     "address": {
    //       // "line1": "14519 Sherman Way",
    //       "city": "Houston",
    //       "state": "CA",
    //       "postal_code": "91405",
    //       "country": "US"
    //     },
    //     "phone": "+12103847937"
    //   }
    // ],
  //   defaultValues: {
  //       "name": "Rudlp",
  //       "address": {
  //         "line1": "14519 Sherman Way",
  //         "city": "Los Angeles",
  //         "state": "CA",
  //         "postal_code": "91405",
  //         "country": "US"
  //       },
  //       "phone": "+19166734562"
  // },
      fields: {
        phone: 'always',
        name: 'never'
      },
      validation: {
        phone: {
        required: 'always'
        }
      }
    },
    confirmParams: {
      return_url: `${window.location.origin}/success`,
      payment_method_data:{
      // billing_details: {
      //     name: "Rudolpho Numbat",
      //     email: "ruddy.numbat@bufo.io"
      //   }
      }
    },
    appearance: {
      rules: {
        '.Label': {
          display: 'none'
        }
      }
    },
    elementsOptions: {
      fonts: [
        {
          family: 'Playwrite AR',
          weight: 400,
          src: "url('https://fonts.googleapis.com/css2?family=Playwrite+AR:wght@100..400&display=swap')"
        }
      ]
    }
  }),
  computed:{
    hasPi() {
      return this.clientSecret !== null
    }
  },
  methods: {
    async generateIntent() {
      if (this.mode === 'setup') {
        await this.generateSetup()
      } else {
        await this.generatePaymentIntent()
      }
      this.mountElements()
    },
    async confirmIntent() {
      if (this.mode === 'setup') {
        await this.confirmSetup()
      } else {
        await this.confirmPayment()
      }
    },
    async generateSetup() {
      const payload = {
        automatic_payment_methods: {
          enabled: true,
        },
        customer: 'cus_OUaIwA7p6JbSxH',
        mode: 'cors'
      }
      const {intent, error} = await this.$axios.$post('/setup_intents/', payload)
      if (error) {
        this.error = error
        return false
      } else {
        this.clientSecret = intent.client_secret
        this.addressOptions.mode = 'billing'
        return true
      }
    },
    async generatePaymentIntent() {
      const payload = {
        amount: this.amount,
        currency: this.currency,
        automatic_payment_methods: {
          enabled: true
        },
        // payment_method_types:['card'],
        description: 'PI for Payment/Address Element testing',
        // "setup_future_usage": "off_session",
        // "customer": "cus_QH7W9qxkhLLWqE"
      }
      const response = await this.$axios.$post('/payment_intents/', payload);
      if (response.error) {
        this.error = response.error
      } else {
        this.clientSecret = response.intent.client_secret
      }
    },
    mountElements() {
      if (this.clientSecret) {
        this.elements = this.$stripe.elements({clientSecret: this.clientSecret, appearance: this.appearance});
        this.paymentElement = this.elements.create('payment', this.paymentOptions);
        this.paymentElement.on('change', (e) => {
          console.log(e)
        })
        console.log(this.paymentElement)
        this.paymentElement.mount('#payment-element')
        console.log(this.addressOptions);
        if (this.collect_address) {
          this.addressElement = this.elements.create('address', this.addressOptions);
        this.addressElement.mount('#address-element');
          this.addressElement.on('change', (e) => {
            console.log(e);
          })
        }

      } else{
        alert('No client secret set')
      }

    },
    async confirmSetup() {
      const resp = await this.$stripe.confirmSetup({
        elements: this.elements,
        confirmParams: this.confirmParams
      })
      console.log(resp);
      if (resp.error) {
        this.error = resp.error
      }
    },
    async confirmPayment() {
      const resp = await this.$stripe.confirmPayment({
        elements: this.elements,
        confirmParams: this.confirmParams
      })
      if (resp.error) {
        this.error = resp.error
      }
    }
  }
}
</script>


