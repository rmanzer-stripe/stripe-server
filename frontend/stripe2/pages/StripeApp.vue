<template>
  <v-row justify="center">
    <v-col cols="12" md="10">
      <p class="text-h2 center-align" v-text="title"></p>
      <v-divider></v-divider>
      <v-card>
        <v-img
        src="https://images.pexels.com/photos/313691/pexels-photo-313691.jpeg?cs=srgb&dl=pexels-energepiccom-313691.jpg&fm=jpg"
        max-height="200"
        gradient="to top right, rgba(0,0,0, 0.7), rgba(0,0,0,0.2)"
        class="white--text align-end"
        >
          <v-card-title>
            Select an Account
          </v-card-title>
          <v-divider class="white"></v-divider>
          <v-card-subtitle>
            Use the select menu below to choose the Account and view daily payment volume
          </v-card-subtitle>
        </v-img>
        <v-card-text>
          <v-row>
            <v-col cols="12" md="4">

            </v-col>
            <v-col cols="12" md="8">
              <v-alert
                v-model="alert"
                border="left"
                close-text="Close Alert"
                type="warning"
                text
                dismissible
              >
                {{message}}
              </v-alert>
              <v-form>
                <v-select v-model="account" :items="accounts" item-text="id" item-value="id" label="Select Account"></v-select>
                <v-btn color="primary" @click="getPayments">
                  <v-icon left>mdi-chart-line</v-icon>
                  Show Volume
                </v-btn>
              </v-form>

            </v-col>
          </v-row>
          <v-sheet v-if="account" color="teal darken-2" elevation="4">
            <v-sparkline
            :value="values"
            :labels="labels"
            line-width="2"
            padding="12"
            color="white"
            label-size="1"
            >
            </v-sparkline>
          </v-sheet>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'StripeApp',
  data: () =>({
    title: 'Stripe App Demo',
    accounts: null,
    url: '/app_accounts',
    account: null,
    payments: [],
    message: null,
    alert: false,
  }),
  computed: {
    // TODO: return an array of objects that contain the TOTAL charges grouped by day
    // First create an array of objects with date strings that span the past 7 days
    // Then run a .map() function on the payments array and add the amount to whichever date strings match the values from the first step
    // Finally use the datestring values as labels and the amounts as values for the v-sparkline component.
    // payment_values() {
    //   if (this.payments.length > 0) {
    //     const map =  this.payments.map(x => {x; return {label: new Date(x.created*1000).toDateString();})
    //     return []
    //   } else {
    //     return []
    //   }
    // }
    values() {
      return this.payments.map(x => x.value)
    },
    labels() {
      return this.payments.map(x => x.label)
    }
  },
  created() {
    this.fetchAccounts();
  },

  methods: {
    async fetchAccounts() {
      this.accounts = await this.$axios.$get(this.url);
    },
    async getPayments() {
      if (this.account !== null) {
        const url = `${this.url}/${this.account}/payments/`
        this.payments = this.transformValues(await this.$axios.$post(url));
      } else {
        this.message = "Select an account first."
        this.alert = true
      }
    },
    transformValues(values) {
      const result = {}
      // const map =  values.map(x => {return {label: new Date(x.created*1000).toLocaleDateString('en-US'), value: x.amount}})

      return result
    }
  },

}
</script>

