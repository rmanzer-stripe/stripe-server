<template>
  <v-container>
    <v-row>
      <v-form>
        <p class="text-h4">Make charge or save bank details</p>

      </v-form>
    </v-row>
    <v-row>
      <v-col cols="12" md="4">
        <v-form>
          <p class="text-h4">Create Payment Intent</p>
          <CustomerSelect ref="customer" class="my-2" />
          <AmountInput ref="amount" class="my-2" />
          <v-switch v-model="sfu" label="Setup Future Usage"></v-switch>
          <v-select v-if="sfu" v-model="sfu_option" :items="sfu_options" item-text="title" item-value="value" label="Select SFU option"></v-select>
          <v-btn color="primary" @click="createPaymentIntent">Create Intent</v-btn>
        </v-form>
      </v-col>
      <v-col cols="12" md="8">
        <v-card>
          <CardHeader :img_height="200" img_src="/images/bank_building.jpeg" img_gradient="to bottom, rgba(0,0,0, 0.1), rgba(0,0,0,0.7)" title_text="ACH Payment Method" title_color="white" />
          <v-card-text>
            <v-form v-if="showForm && !showMandate" ref="accountForm">
              <p class="text-h4">Enter Account Holder Details</p>
              <v-text-field :rules="[v => !!v || 'Required']" label="Name" v-model="account.name" append-icon="mdi-account" />
              <v-text-field :rules="[v => !!v || 'Required']" label="Email" v-model="account.email" append-icon="mdi-at" />
              <v-btn color="primary" @click="collectAccount">Collect Account Info</v-btn>
            </v-form>
            <v-form v-else-if="showForm && showMandate" ref="mandateForm">
              v-text-field
              <v-alert border="left" type="info" colored-border elevation="2">
                By clicking [accept], you authorize Supermanzer LLC to debit the bank account specified above for any amount owed for charges arising from your use of Supermanzer LLC's services, pursuant to Supermanzer LLC's website and terms, until this authorization is revoked. You may amend or cancel this authorization at any time by providing notice to Supermanzer LLC with 30 (thirty) days notice.
              </v-alert>
              <v-checkbox v-model="acceptMandate" :rules="[v => !!v || 'Required']" @click="confirmAccount">
                <template v-slot:label>
                  <div>
                    I accept
                  </div>
                </template>
              </v-checkbox>
            </v-form>
            <div v-else-if="showStatusAlert">
              <v-alert v-if="paymentIntent.status === 'processing'" border="left" colored-border icon="mdi-warning" color="amber">
                The Payment Intent is processing
              </v-alert>
              <v-alert v-else-if="paymentIntent.status === 'succeeded'" border="left" type="success">
                Payment Intent was successful
              </v-alert>
              <v-btn color="primary" @click="getStatus" >
                <v-icon>mdi-refresh</v-icon>
                Refresh Status</v-btn>
            </div>
            <v-alert v-else type="info" border="left">
              Form for needed info will be loaded once the Payment Intent is created
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

  </v-container>
</template>

<script>
  import CardHeader from '../core/CardHeader.vue';
import AmountInput from './AmountInput.vue';
import CustomerSelect from './CustomerSelect.vue';


export default {
    name: "AchDirectDebit",
    components: { AmountInput, CardHeader, CustomerSelect },
    data: () => ({
      // clientSecret: null,
      paymentOrSetup: false,
      paymentIntent: null,
      sfu: false,
      sfu_options: [
        {value:'off_session', title: 'Off Session'},
        {value: 'on_session', title: 'On Session'}
      ],
      sfu_option: null,
      account: {
        name: null,
        email: null
      },
      showMandate: false,
      acceptMandate: false,
      interval: null
    }),
    computed: {
      showForm() {
        return this.paymentIntent !== null && !this.showStatusAlert
      },
      showStatusAlert() {
        if (this.paymentIntent !== null) {
          return (this.paymentIntent.status === 'processing' || this.paymentIntent.status === 'succeeded')
        } else {
          return false;
        }

      }
    },
    methods: {
      getParams() {
        const params = {
          amount: this.$refs.amount.amount,
          currency: 'usd',
          payment_method_types: ['us_bank_account'],
          payment_method_options: {
            us_bank_account: {
              financial_connections: {
                permissions: ["payment_method", "balances"]
              }
            }
          }
        }
        if (this.sfu) {
          params.setup_future_usage = this.sfu_option
        }
        if (this.$refs.customer.selectedCustomer.id !== undefined) {
          params.customer = this.$refs.customer.selectedCustomer.id
        }
        return params
      },
      async createPaymentIntent() {
        const params = this.getParams()
        const pi = await this.$axios.$post('payment_intents/', params)
        this.paymentIntent = pi
      },
      async collectAccount(){
        const {paymentIntent, error} = await this.$stripe.collectBankAccountForPayment({
          clientSecret: this.paymentIntent.client_secret,
          params: {
            payment_method_type: 'us_bank_account',
            payment_method_data: {
              billing_details: {
                name: this.account.name,
                email: this.account.email
              }
            }
          },
          expand: ['payment_method']
        })
        if (error) {
          console.error(error);
        } else {
          this.paymentIntent = paymentIntent;
          switch(paymentIntent.status) {
            case 'requires_confirmation':
              this.showMandate = true
              break;
            case 'requires_payment_method':
              this.$refs.accountForm.reset();
              break;
          }
          console.log(paymentIntent);
        }
      },
      async confirmAccount() {
        const {paymentIntent, error} = await this.$stripe.confirmUsBankAccountPayment(this.paymentIntent.client_secret)
        if (error) {
          console.log(error);
        } else {
          this.paymentIntent = paymentIntent;
          this.showMandate = false;
          switch (paymentIntent.status) {
            case 'requires_payment_method':
              console.log(paymentIntent);
              break;
            case 'processing':
              this.status = paymentIntent;

              break;
            case 'requires_action':
              if (paymentIntent.next_action?.tpe === 'verify_with_microdeposits') {
                console.log("Need to verify account with microdeposits");
              }
              console.log(paymentIntent);
              break;
          }
        }
      },
      async getStatus() {
          const intent = await this.$stripe.retrievePaymentIntent(this.paymentIntent.client_secret);
          this.paymentIntent = intent
      }
    }
}
</script>
