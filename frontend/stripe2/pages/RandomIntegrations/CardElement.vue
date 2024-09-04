<template>
  <v-row justify="center">
    <v-col cols="12" sm="6">
      <v-card>
        <v-card-title>Card Element Integration</v-card-title>
        <v-card-subtitle>Using the old Card Element {{ flow_label }}</v-card-subtitle>
        <v-card-text>
          <p class="h1">FUNKY STUFF!</p>
          <div>
            This is where the card element will be rendered but first let's make some choices about what we're going to do
            <v-form>
              <v-row>
                <v-col cols="12" sm="5">
                  <v-radio-group v-model="flow_option">
                    <v-radio v-for="o in flowOptions" :key="o" :label="o" :value="o"></v-radio>
                  </v-radio-group>
                </v-col>
                <v-col cols="12" sm="7">
                  <customer-select v-show="flow_option == 'create_attach_pm'" @customer-selected="setCustomer"></customer-select>
                </v-col>
              </v-row>
            </v-form>
          </div>
          <div id="card-element"></div>
        </v-card-text>
        <v-card-actions>
          <v-btn color="teal" @click="setFlow" class="white--text">Load Element</v-btn>
          <v-btn color="primary" @click="cardElementAction" :disabled="cardElement == null">Submit</v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>

</template>

<script>
import CustomerSelect from '~/components/stripe/CustomerSelect.vue';

export default {
  components: {CustomerSelect  },
  data: () => ({
    clientSecret: null,
    elements: null,
    cardElement: null,
    postalCode: '',
    flowOptions: [
      'confirm_payment',
      'confirm_setup',
      'charge_with_token',
      'create_payment_method',
      'create_attach_pm'
    ],
    flow_option: null,
    customer: null

  }),
  computed: {
    flow_label(){
      if (this.flow_option !== null) {

        let label_str = `${this.flow_option}`
        if (this.customer !== null) {
          label_str += `- ${this.customer.id}`
        }
        return label_str
      } else {
        return ""
      }
    }
  },
  created() {
    // const {intent} = await this.$axios.$post('/payment_intents/', {amount: 1099, currency: 'usd'})
    // this.clientSecret = intent.client_secret
    // this.elements = this.$stripe.elements({clientSecret: this.clientSecret})
    this.elements = this.$stripe.elements()
  },
  methods: {
    setCustomer(cust) {
      this.customer = cust
    },
    async setFlow(){
      this.cardElement = this.elements.create('card', {hidePostalCode: false, hideIcon: false})
      this.cardElement.mount('#card-element')
      const {intent} = await this.$axios.$post('/payment_intents/', {amount: 1099, currency: 'usd'})
      this.clientSecret = intent.client_secret
    },
    cardElementAction() {
      switch (this.flow_option) {
        case 'create_attach_pm':
          this.createAttach()
          break;

          case 'confirm_payment':
            this.cardPayment()
            break;

        default:
          break;
      }
    },
    async createAttach() {
      const pm = await this.$stripe.createPaymentMethod({
            type: 'card',
            card: this.cardElement,
            billing_details: {
              name: this.customer.name
            }
          })
          console.log(pm);
    },
    async cardPayment() {
      try {
        // Display loader
        const response = await this.$stripe.confirmCardPayment(this.clientSecret, {
          payment_method: {
            card: this.cardElement,
            // billing_details: { address: { postal_code: this.postalCode } },
          },
        });

        if (response.error) {
          // Hide loader
          // Display error message
          console.log(response);
        } else {
          // Poll the backend every 500 milliseconds to see if the webhook we_1ImnCIKle9HVUxsx0P0KCpm6 has been received confirming the payment is successful
          // Once confirmed as successful:
          // - Hide loader
          // - Redirect user to success page
        }
      } catch (error) {
        // Hide loader
        // Display error message
        console.log(error);
      }
    }
  }
}
</script>
