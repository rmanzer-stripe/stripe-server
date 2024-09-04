<template>
  <v-card class="mx-auto">
    <v-img
      height="350px"
      src="https://images.pexels.com/photos/262488/pexels-photo-262488.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
      class="white--text align-end"
      gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.8)"
    >
      <v-card-title>Connect Integrations</v-card-title>
    </v-img>
    <v-container class="my-5">
      <v-row>
        <ErrorAlert :error="error" />
        <!-- Notification -->
        <v-alert v-model="showNotification" :type="notification.type" dismissible outlined border="left" colored-border width="100%">
          <p>{{ notification.text }}</p>
        </v-alert>
        <v-alert
                v-if="component === 'account-onboarding' && sessionSecret == null"
                type="info"
                outlined
                border="left"
                colored-border
                >
                <p class="text-h4">New Account will be created</p>
                <v-divider></v-divider>
                <p>In order to go through a proper onboarding flow, creating an account session for the `account-onboarding` component will also create a new Connect Account.</p>
                <p>The account creation parameters are shown below</p>
                <code>
                  {{ account_params }}
                </code>
              </v-alert>
        <div id="notification-banner" ref="notification_banner"></div>
      </v-row>
      <v-row>
        <v-card  width="100%" class="mb-6" flat>
          <v-row justify="space-between">
            <div>
              <v-card-title>Connect Embedded Components</v-card-title>
              <v-card-subtitle>Embed elements of the Connect Dashboard in your own site</v-card-subtitle>
            </div>
            <!-- <div>
              <p>Need to create some payments?</p>
              <v-btn color="primary" dark  icon>
                <v-icon>mdi-help</v-icon>
              </v-btn>
            </div> -->


        </v-row>
          <v-card-text class="my-4">
            <v-row class="mx-4">
              <v-col cols="12" sm="4" class="">

                <v-form>
                  <v-select
                  v-model="connectAccount"
                  label="Select Connect Account"
                  :items="connectAccounts"
                  item-title="id"
                  item-value="email"
                  :hint="`${connectAccount.email} - ${connectAccount.type} - ${connectAccount.country} - ${connectAccount.id}`"
                  persistent-hint
                  return-object
                  single-line
                  disabled
                  ></v-select>
                  <v-select v-model="component" :items="components" label="Select Connect Component" class="my-5"></v-select>

                </v-form>

                  <v-btn @click="createSession" color="indigo" class="white--text my-2" >Create Session</v-btn>
                  <v-btn @click="mountComponent" color="teal" class="white--text my-4" :disabled="sessionSecret == null">Mount Component</v-btn>


                <!-- <account-get-create @account-select="setAccount" /> -->
              </v-col>
              <v-col cols="12" sm="8" >
                <div ref="connect_container" height="100%">
                  <v-card width="100%" height="100%" class="indigo lighten-4 ">
                    <v-card-text>
                      Placeholder content  Embedded Elements go here
                    </v-card-text>
                  </v-card>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions>

          </v-card-actions>
        </v-card>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
import ErrorAlert from '~/components/stripe/ErrorAlert.vue';

export default {
  name: "StripeConnect",
  components: {
    ErrorAlert,
    // AccountGetCreate
  },
  data: () => ({
    containerId: 'connect-containr',
    stripeConnect: null,
    sessionSecret: null,
    connectInstance: null,
    componentInstance: null,
    // Hard-coding for now, will make dynamic later
    // connectAccount: {id: 'acct_1Kr3CJRSxigF24b2'}, // currently_due, eventually_due, past_due
    // connectAccount: {id: 'acct_1KP7l0RG7epvfalf'},
    // connectAccount: {id: 'acct_1PSoNOIejxrDoAL9'}, // Just onboarded
    connectAccount: {id: 'acct_1PSnhWIpjNN4TwEF'}, // Just 'eventually_due'
    // connectAccount: {id:'acct_1PVdm7IuDUcdVUpm'}, // Federico Platypus
    // connectAccount: {id: 'acct_1P1AFAI14UbDWec5'}, // rando test
    // connectAccount: {id: 'acct_1PSoIwIJM2Cl7yuC'}, // Custom account
    connectAccounts: null,
    error: null,
    notification: {
      type: "info",
      text: "",
    },
    showNotification: false,
    components: [
      {
        text: "Account management",
        value: "account-management"
      },
      {
        text: "Account onboarding",
        value: 'account-onboarding'
      },
      {
        text: "Account balances",
        value: "balances"
      },
      {
        text: "Payments List",
        value: "payments"
      },
      // TODO: Decide how to implement payment details section: how to decide what Payment Intent to display?
      // https://docs.stripe.com/connect/supported-embedded-components/payment-details
      {
        text: 'Payouts',
        value: 'payouts'
      },
      {
        text: "Documents",
        value: 'documents'
      },
      {
        text: "Notifications",
        value: 'notification-banner'
      }
    ],
    component: null,
    banner: null,
    account_params : {
      controller: {
        fees: { payer: 'application'},
        losses: { payments: 'application'},
        requirement_collection: 'application',
        stripe_dashboard: { type: 'none' }
      },
      capabilities: {
        transfers: { requested: true},
        card_payments: {requested: true}
      }
    }

}),
  created() {
    this.getAccounts()
  },
  methods: {
    async getAccounts() {

      let {results} = await this.$axios.$get('/connect-accounts/')
      results = results.map(x => x.data)
      this.connectAccounts = results
    },
    async createAccount(){

      const { account } = await this.$axios.$post('/connect-accounts/', this.account_params)
     return account
    },
    async createSession() {
      // TODO: check if selected component is Connect onboarding and
      // create an account in that case.
      if (this.component === null) {
        this.error = {
          code: 'missing_component',
          type: 'invalid_configuration',
          message: 'No component specified.  Please select a component before creating an Account Session.'
        }
        return;
      }
      if (this.component === 'account-onboarding') {
        const account = await this.createAccount()
        this.connectAccount = account
      }
      if (Object.keys(this.connectAccount).length === 0) {
        this.error = {message: "No Connect Account selected.  Select account first.", code: 'invalid_request'}
      } else {
        await this.getAccountSession()
        if (this.sessionSecret !== null) {
          this.connectInstance = window.StripeConnect.init({
            publishableKey: "pk_test_51JticYIlCeH6bP8REulC9GlUO09hWuGsCljwJ3VNWhqqLmTTW0CedWXOoABWyXkplmqMtwfA4SiXkdeqCMvesIii00BCpJb9Vb",
            clientSecret: this.sessionSecret,
            refreshClientSecret: this.getAccountSession,
            appearance: {
            // variables: {
            //   badgeSuccessColorBackground: "#000000",
            //   badgeSuccessColorText: "#00FF00",
            // },
          },
          })
          this.notification = {type: 'success', text:"Stripe Connect initialized"}
        } else {
          this.notification = {msg: 'No Account Session client secret provided', type: 'error'}
        }
        this.showNotification = true
      }
    },
    async getAccountSession() {
      const url = `/connect-accounts/${this.connectAccount.id}/account_session/`
      const payload = {component: this.component}
      try {
        const response = await this.$axios.$post(url, payload)
        this.sessionSecret = response.client_secret
        this.notification = {type: 'info', text: 'Connect Account Session created'}
      } catch (e) {
        this.notification = {type: 'error', text: e.msg}
      }
      this.showNotification = true
      //
    },
    async initConnect() {
      if (this.sessionSecret) {
        this.connectInstance = await this.stripeConnect.initialize({
          publishableKey: "pk_test_51JticYIlCeH6bP8REulC9GlUO09hWuGsCljwJ3VNWhqqLmTTW0CedWXOoABWyXkplmqMtwfA4SiXkdeqCMvesIii00BCpJb9Vb",
          clientSecret: this.sessionSecret,
          refreshClientSecret: this.getAccountSession
        })
        this.notificationBanner = this.connectInstance.create('notification-banner');
        this.$refs.notification_banner.appendChild(this.notificationBanner)

        this.notification = {type: 'success', text:"Stripe Connect initialized"}
      } else {
        this.error = {msg: 'No Account Session client_secret available', type: 'error'}
        return "Failure"
      }
      this.showNotification = true
    },
    loadOnboarding() {
      this.onboardingInstance = this.connectInstance.create('stripe-connect-account-onboarding');
      this.onboardingInstance.addEventListener('exit', () => {
        console.log("User exited onboarding flow");
      })
      document.getElementById('onboarding').appendChild(this.onboardingInstance)
      this.notification = {type: 'info', text: 'Connect onboarding initialized'}
    },
    logNotificationBanner(response){
      console.log(response);
    },
    logOnLoaderStart(event){
      console.log(event);
      console.log(`${event.elementTagName} is visible to users`)
    },
    mountComponent() {
      if (this.component === null || this.connectInstance === null) {
        this.notification = {type: 'error', text: "Either connect not initialized or component not selected. Do those things first"}
      } else {
        this.clearContainer()
        this.componentInstance = this.connectInstance.create(this.component)
        if (this.componentInstance !== null) {
          if (this.component === "notification-banner") {
            const options = {
              fields: 'eventually_due',
              futureRequirements: 'include'
            }
            this.componentInstance.setCollectionOptions(options)
            this.componentInstance.onNotificationsChange((event)=> {this.logNotificationBanner(event)})
          }
          this.componentInstance.setOnLoaderStart((event) => {this.logOnLoaderStart(event)})
          this.$refs.connect_container.appendChild(this.componentInstance)
        } else {
          this.notification = {type: 'error', text: 'Component Instance not created'}
        }

      }
    },
    clearContainer() {
      this.$refs.connect_container.innerHTML = ""
    },
    logout() {
      this.connectInstance.logout()
      this.componentInstance = null
    }
  },

}
</script>
