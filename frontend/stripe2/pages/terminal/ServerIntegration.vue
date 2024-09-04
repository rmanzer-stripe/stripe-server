<template>
  <v-container fluid>
    <v-row justify="center" align="center">
      <v-col align-self="center" cols="12" sm="12" md="10">
        <v-card>
          <v-img
            class="align-end white--text" height="400" gradient="to top, rgba(0,0,0, 0.7), rgba(0,0,0,0.2)"
            src="https://images.pexels.com/photos/1148820/pexels-photo-1148820.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1">
            <v-card-title class="text-h4">Server Side Terminal Integration</v-card-title>
          </v-img>
          <v-card-text>
            <v-row>
              <v-col cols="12" sm="12" md="8" align-self="center">
                <ReaderStatus :reader-id="readerId" />
                <reader-selector v-if="readers.length > 1" :readers="readers" @change="setReader($event)" />
                <error-alert :error="error" />
              </v-col>
              <v-col cols="12" sm="12" md="4">

                <AmountInput ref="amount" />
                <v-select v-model="currency" :items="currencies" label="Select Currency" />
                <v-switch v-model="autoCapture" label="Automatic Capture" ></v-switch>
              </v-col>
            </v-row>
            <v-row align="center" justify="center" class="pa-5">
              <v-col cols="12" sm="12">
                <v-alert v-if="message !== null" type="info" colored-border border="left" elevation="3">{{ message }}</v-alert>
              </v-col>

              <v-col cols="12" sm="6">
                <p class="text-h5 center-align">Stripe Object</p>
              </v-col>
              <v-col cols="12" sm="6">
                <v-btn-toggle v-model="stripeObject" tile color="deep-purple accent-3" group>
                  <v-btn :value="reader">Reader</v-btn>
                  <v-btn :value="paymentIntent">Payment Intent</v-btn>
                  <v-btn :value="setupIntent">Setup Intent</v-btn>
                </v-btn-toggle>
              </v-col>
              <v-col cols="12" sm="12" max-height>
                <v-card max-height="600">
                  <v-card-text class="py-4">
                    <pre class="code">{{stripeObject}}</pre>
                  </v-card-text>
                </v-card>
              </v-col>

            </v-row>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-row align="center" justify="space-around" class="ma-4">

              <v-btn color="primary" class="ma-4" :loading="connectLoading" @click="getReader">
                <v-icon>mdi-connection</v-icon>
                Retrieve Reader(s)
              </v-btn>
              <v-btn color="blue-grey" class="white--text ma-4" :loading="fetchIntentLoading" @click="getPaymentIntent">
                Fetch PI
              </v-btn>
              <v-btn color="deep-purple" class="white--text ma-4" @click="getSetupIntent">Fetch SI</v-btn>
              <v-btn color="green" class="white--text ma-4" :loading="processPaymentLoading" @click="processIntent">
                Process Intent
              </v-btn>
              <v-btn color="secondary" class="ma-4" @click="updateIntent">Refresh Intent</v-btn>
              <v-btn color="teal lighten-200" class="white--text ma-4" @click="captureIntent"> Capture Intent</v-btn>
              <v-btn class="gd-winterneva white--text" @click="cancelAction">Cancel Action</v-btn>
            </v-row>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ReaderStatus from '../../components/terminal/ReaderStatus.vue';
import AmountInput from '~/components/stripe/AmountInput.vue';
import ReaderSelector from '~/components/terminal/ReaderSelector.vue';
import ErrorAlert from '~/components/stripe/ErrorAlert.vue';


export default {
  name: 'ServerIntegration',
  components: { AmountInput, ReaderStatus, ReaderSelector, ErrorAlert,  },
  async asyncData({ $axios}) {
    const {results} = await $axios.$get('/products/')
    return { products: results}
  },
  data: () => ({
    reader: null,
    currencies: ['USD', 'CAD', 'EUR'],
    currency: 'USD',
    paymentIntent: null,
    setupIntent: null,
    connectLoading: false,
    fetchIntentLoading: false,
    processPaymentLoading: false,
    autoCapture: false,
    stripeObject: {},
    readers: [],
    message: null,
    error: null

  }),
  computed: {
    readerAvailable() {
      return this.reader !== null
    },
    readerId() {
      if (this.reader !== null) {
        return this.reader.id
      } else {
        return null
      }
    },
    captureMethod() {
      return this.autoCapture ? "automatic": "manual"
    }
  },
  methods: {
    async getReader() {
      this.connectLoading = true;
      const {data} = await this.$axios.$get("/terminals/");
      if (data) {
        if (data.length > 1) {
          this.readers = data
          this.message = "Select a reader from the menu"
        } else {
          this.reader = data[0]
        }
      } else {
        console.error("Error")
      }
      this.connectLoading = false;
    },
    setReader(evt){
      console.log(evt);
      this.reader = evt
      this.stripeObject = this.reader
      this.message = null
    },
    async getPaymentIntent() {
      this.fetchIntentLoading = true;
      const payload = {
        capture_method: 'manual',
        payment_method_types: [ 'card_present'],
        setup_future_usage: "off_session",
        currency: this.currency,
        amount: Number(this.$refs.amount.amount)
      }
      try {
        const {intent} = await this.$axios.$post('/payment_intents/', payload);
        this.paymentIntent = intent
        this.fetchIntentLoading = false;
        this.stripeObject = this.paymentIntent
      } catch (error) {
        this.error = error.response.data.error
        this.fetchIntentLoading = false;
      }
    },
    async getSetupIntent() {
      const payload = {
        payment_method_types: ['card_present'],
        // customer: 'cus_OUaIwA7p6JbSxH'
      }
      try {
        const data = await this.$axios.$post('/setup_intents/', payload)
        this.setupIntent = data
        this.stripeObject = this.setupIntent
      } catch (error) {
        this.error = error.response.data.error
      }
    },
    async processIntent() {
      if (this.paymentIntent) {
        const url = `/terminals/${this.reader.id}/process_intent/`
        const payload = {
          payment_intent: this.paymentIntent.id
        }
        await this.$axios.$post( url, payload)
      } else if(this.setupIntent){
        const url = `/terminals/${this.reader.id}/process_intent/`
        const payload = {
          setup_intent: this.setupIntent.id,
          customer_consent_collected: true
        }
        await this.$axios.$post(url, payload)
      } else {
        this.message = "You're going to need a Payment Intent first.  Try fetching one"
      }

    },
    async updateIntent() {
      if (this.paymentIntent) {
        this.paymentIntent = await this.$axios.$get(`/payment_intents/${this.paymentIntent.id}/`)
        this.stripeObject = this.paymentIntent
      } else if (this.setupIntent) {
        this.setupIntent = await this.$axios.$get(`/setup_intents/${this.setupIntent.id}/`)
        this.stripeObject = this.setupIntent
      } else {
        this.error = {msg: 'No intent to update'}
      }
    },
    async captureIntent() {
      if (this.paymentIntent) {
        const params = {amount_to_capture: this.paymentIntent.amount, capture: true}
        const { msg } = await this.$axios.$post(
          `/payment_intents/${this.paymentIntent.id}/capture/`, params
          )
          this.message = msg
      } else {
        this.message = "No Payment Intent to capture"
      }

    },
    async cancelAction(){
      if (this.reader !== null) {
        const url = `terminals/${this.reader.id}/cancel_action/`
        const resp = await this.$axios.$post(url)
        console.log(resp)
      }
    }
  },
}
</script>

<style scoped>
pre {
  border: 2px black;
  background-color: #123236;
  color: greenyellow;
  overflow-x: auto;
}
html {
  overflow: hidden !important;
}

.v-card {
  display: flex !important;
  flex-direction: column;
}

.v-card__text {
  flex-grow: 1;
  overflow: auto;
}
.gd-winterneva {
  background-image: linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%);
}
</style>
