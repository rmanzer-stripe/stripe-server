<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="8">
      <v-card>
        <v-img
          height="500"
          src="https://images.pexels.com/photos/3767229/pexels-photo-3767229.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
          class="white--text align-end" gradient="to top right, rgba(100,115,201,.33), rgba(25,32,72,.7)">
          <v-card-title>
            Terminal Operations
          </v-card-title>
          <v-divider color="white"></v-divider>
          <v-card-subtitle class="white--text">Perform all basic JS integrations with your Wise POS E</v-card-subtitle>
        </v-img>
        <v-card-text>
          <v-row justify="center" align="center" height="60">
            <v-col cols="12" sm="12" md="8">
              <CoreAlert v-if="hasMessage" v-model="alert" :alert-type="alertType" :message="message" />
            </v-col>
          </v-row>
          <v-row justify="center">
            <v-col cols="12" sm="12" md="10">
              <p class="text-h4">Pre-Charge Actions</p>
              <v-btn color="primary" @click="initializeTerminal">
                <v-icon>mdi-reload</v-icon>
                Initialize Terminal
              </v-btn>
              <v-btn v-if="!hasReaders" color="secondary" outlined @click="discoverReaders">
                <v-icon>
                  mdi-book-search
                </v-icon>
                Discover Readers
              </v-btn>
              <v-tooltip right>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn color="teal darken-2" outlined v-bind="attrs" @click="simulateReader"  v-on="on" >
                    <v-icon>
                      mdi-book-search
                    </v-icon>
                    Simulate Reader
                  </v-btn>
                </template>
                <span>Simulate full payment collection/processing</span>
              </v-tooltip>
            </v-col>
          </v-row>
          <v-row justify="center" align="center" class="mx-4">
            <v-col cols="12" sm="12" md="8">
              <v-select
                v-model="selectedReader" :items="readers" item-text="label" item-value="id" return-object
                label="Select Your Reader" no-data-text="No Readers Detected......Try Discovering Some"></v-select>
            </v-col>
            <v-col cols="12" md="4">

              <v-btn v-if="!hasReader && hasReaders" color="success" outlined @click="connectReader">Connect Reader
              </v-btn>
            </v-col>
          </v-row>
          <TerminalPresets @click="setAmount" />
        </v-card-text>
        <v-form>
          <p class="h4 mx-8">Specify Charge to be Made</p>
          <v-row class="mt-4" justify="center">
            <v-col cols="12" sm="12" md="4">
              <v-text-field v-model="amount" type="number" label="Amount to Charge" hint=""></v-text-field>
            </v-col>
            <v-col cols="12" sm="12" md="4">
              <v-select
                v-model="currency" :items="currencies" item-text="name" item-value="code" single-line
                label="Currency to Charge"></v-select>
            </v-col>
          </v-row>
          <v-row justify="center">
            <v-col cols="12" sm="6" md="4">
              <v-checkbox
                v-model="future_use" :label="`Save card for future use: ${future_use.toString()}`"
                color="success"></v-checkbox>
            </v-col>
          </v-row>
        </v-form>
        <v-divider></v-divider>
        <v-card-actions class="d-flex justify-space-around py-4">
          <v-btn color="info" outlined @click="configTipping">
            Add tips to Reader
          </v-btn>
          <v-btn color="warning" outlined @click="cancelPayment">
            Cancel Payment
          </v-btn>
          <v-btn color="success" outlined @click="collectPayment">
            <v-icon>
              mdi-smart-card-reader-outline
            </v-icon>
            Collect Payment
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'JsIntegration',
  data: () => ({
    readers: [],
    reader: null,
    selectedReader: null,
    secret: '',
    location: '',
    message: '',
    alertType: 'error',
    amount: 2099,
    currency: 'usd',
    future_use: false,
    terminal: null,
    currencies: [
      { code: 'usd', name: 'US Dollar' },
      { code: 'eur', name: 'Euro' },
      { code: 'cad', name: "Canadian Dollar" }
    ],
    loading: false,
    alert: true,
  }),
  computed: {
    hasMessage() {
      return this.message.length > 0
    },
    hasReaders() {
      return this.readers.length > 0
    },
    hasReader() {
      return this.reader !== null
    },
    hasTerminal() {
      return this.terminal !== null
    }
  },
  methods: {
    initializeTerminal() {
      /* eslint no-undef: 0 */
      this.terminal = StripeTerminal.create({
        onFetchConnectionToken: this.getConnectionToken,
        onUnexpectedReaderDisconnect: this.unexpectedDisconnect,
        readerBehavior: {allowCustomerCancel: true}
      })
      this.message = 'Terminal initialized'
      this.alertType = 'info'
    },
    async getConnectionToken() {
      const token = await this.$axios.$post('/terminals/connection_token/')
      this.secret = token.secret
      return token.secret
    },
    async configTipping() {
      const result = await this.$axios.$post('/terminals/configure/')
      const alertType = result.status === 'Succeeded' ? 'success' : 'error'
      const message = result.status === 'Succeeded' ? result.message : result.error
      this.showAlert({
        msg: message,
        alertType
      })
    },
    showAlert({ msg, alertType }) {
      this.message = msg
      this.alertType = alertType
      this.alert = true
    },
    unexpectedDisconnect() {
      this.showAlert({
        msg: "The Stripe Terminal reader has unexpectedly disconnected.  Please check connection status.",
        alertType: "warning"
      })
    },
    async discoverReaders() {
      this.loading = true
      if (this.terminal === null) {
        this.initializeTerminal()
      }
      const { discoveredReaders } = await this.terminal.discoverReaders();
      this.readers = discoveredReaders
      if (this.readers.length > 0) {
        this.showAlert({
          msg: "Readers discovered! Now select one to connect",
          alertType: 'success'
        })
      }
      this.loading = false
    },
    async connectReader() {
      this.loading = true
      if (this.selectedReader === null) {
        this.showAlert({
          msg: 'No reader selected',
          alertType: 'error'
        })
        this.loading = false
        return null
      }
      const { reader, error } = await this.terminal.connectReader(this.selectedReader)
      if (error) {
        this.showAlert({
          msg: `Failed to connect: ${error.code} - ${error.message}`,
          alertType: 'error'
        })
        this.loading = false
      } else {
        this.reader = reader
        this.message = `Connected to reader: ${reader.label}`
        this.alertType = 'success'
        this.showAlert({
          msg: `Connected to reader: ${reader.label}`,
          alertType: 'success'
        })
        this.loading = false
      }
    },

    displayReader() {
      this.terminal.setReaderDisplay({
        type: 'cart',
        cart: {
          line_items: [
            {
              description: "Caramel latte",
              amount: 659,
              quantity: 1,
            },
            {
              description: "Dozen donuts",
              amount: 1239,
              quantity: 1,
            },
          ],
          tax: 100,
          total: 1998,
          currency: 'usd',
        },
      });
    },
    async createSubscription() {
      // TODO: Implement this
    },
    async createPaymentIntent() {
      const payload = {
        customer: 'cus_MuAXDk5qaM3Lv8',
        amount: this.amount,
        currency: this.currency,
        payment_method_types: ['card_present', 'card'],
        capture_method: 'manual',
        enable_automatic_capture: true
      }
      if (this.future_use) {
        payload.setup_future_usage = "off_session"
      }
      const pi = await this.$axios.$post(
        '/payment_intents/',
        payload
      )
      return { pi }
    },
    async collectPayment() {
      this.displayReader()

      const { pi } = await this.createPaymentIntent()

      const {obj} = await this.terminal.collectPaymentMethod(pi.client_secret)
      console.log(obj);
      if (obj.error) {
        this.showAlert({
          msg: `Error: ${error.code} ${error.message}`,
          alertType: 'error'
        })
      } else {
        const response = await this.terminal.processPayment(obj.paymentIntent);
         console.log(response)
        if (response.error) {
          this.showAlert({
            msg: `Error: ${error.code} ${error.message}`,
            alertType: 'error'
          })
        } else {
          const captureResponse = await this.capturePayment(response.paymentIntent.id)
          console.log(captureResponse);
          if (captureResponse.status === 500) {
            this.showAlert({
              msg: `Error: ${captureResponse.msg}`,
              alertType: 'error'
            })
          } else {
            this.showAlert({
              msg: `${captureResponse.msg}`,
              alertType: 'success'
            })
          }
        }
      }
    },
    async cancelPayment() {
      const cancelResponse = await this.terminal.cancelCollectPaymentMethod()
      console.log(cancelResponse);
    },
    async collectTerminalPM(terminal, intent) {
      return await terminal.collectPaymentMethod(intent.client_secret)
    },
    // async terminalProcessPayment(terminal, intent) {
    //   return await terminal.processPayment(intent)
    // },
    async capturePayment(id) {
      return await this.$axios.$post(`/payment_intents/${id}/capture/`, { capture: true })
    },
    setAmount(e) {
      this.amount += e;
    },
    handleError(terminal, error) {
      const status = error.paymentIntent.status
      const intent = error.paymentIntent
      switch (status) {
        case 'requires_payment_method':
          this.message = "Please provide a different payment method"
          this.alertType = "info"
          this.showAlert({
            msg: "Please provide a different payment method",
            alertType: 'info'
          })
          this.collectTerminalPM(terminal, intent)
          break;
        case 'requries_confirmation':
          this.terminalProcessPayment(terminal, intent)
          break;
        default:
          this.message = "Something appears to have gone wrong.  Time for a coffee break."
          this.alertType = "error"
          this.showAlert({
            msg: "Something appears to have gone wrong.  Time for a coffee break.",
            alertType: "error"
          })
          break;
      }
    },
    async simulateReader(){
      if (this.terminal === null) {
        alert('Initialize Terminal First')
        return null;
      }
      const config = {simulated: true}
      const discoverResult = await this.terminal.discoverReaders(config)
      console.log(discoverResult);
      if (discoverResult.error) {
        console.error(discoverResult.error)
      } else if (discoverResult.discoveredReaders.length === 0) {
        console.log("NO available readers");
      } else {
        this.reader = discoverResult.discoveredReaders[0]
        const connectResult = await this.terminal.connectReader(this.reader)
        console.log('Connection Result');
        console.log(connectResult);
        this.terminal.setSimulatorConfiguration({testCardNumber: '4242424242424242'})
        const { pi } = await this.createPaymentIntent()
        console.log("Payment Intent");
        console.log(pi);
        const collectResult = await this.terminal.collectPaymentMethod(pi.client_secret)
        console.log("Connection Result");
        console.log(collectResult);
        if (collectResult.error) {
          console.error(collectResult.error)
        } else {
          const processResult = await this.terminal.processPayment(collectResult.paymentIntent)
          console.log("Process Result");
          console.log(processResult);
          if (processResult.error) {
            console.error(processResult.error)
          } else {
            const captureResult = await this.capturePayment(processResult.paymentIntent.id)
            console.log('Capture Result')
            console.log(captureResult);
            if (captureResult.status === 500) {
              console.error(captureResult.msg)
            } else {
              console.log(captureResult.msg)
            }
          }
        }
      }
    }
  },

}
</script>
