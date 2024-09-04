<template>
    <v-card class="px-4">
      <v-expansion-panels flat>
        <v-expansion-panel>
          <v-expansion-panel-header>
            <v-card-title>
              Create Customer
            </v-card-title>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-card-text>
              <v-form>
                <v-row>
                  <v-col cols="12" md="4" sm="6">
                    <v-text-field v-model="customer_data.name" label="Customer Name"></v-text-field>
                  </v-col>
                  <v-col cols="12" md="4" sm="6">
                    <v-text-field v-model="customer_data.email" label="Customer Email" required></v-text-field>
                  </v-col>
                  <v-col cols="12" md="4" sm="6">
                    <v-text-field v-model="customer_data.coupon" label="Coupon ID (if any)"></v-text-field>
                  </v-col>
                  <v-col cols="12" md="4" sm="6">
                    <v-text-field v-model="customer_data.payment_method" label="Payment Method ID" hint="Enter Payment Method ID to attach to Customer" persistent-hint></v-text-field>
                  </v-col>
                  <v-col cols="12" md="4" sm="6">
                    <v-text-field v-model="customer_data.test_clock" label="Test clock ID" hint="Enter Test Clock ID to attach to Customer" persistent-hint></v-text-field>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col>
                    <v-form>
                      <v-text-field v-model="mkey" label="Metadata key"></v-text-field>
                      <v-text-field v-model="mvalue" label="Metadata value"></v-text-field>
                      <v-btn @click="append_key_value">Append</v-btn>
                    </v-form>
                  </v-col>
                  <v-col>
                    <pre>{{ customer_data.metadata }}</pre>
                  </v-col>
                </v-row>
                <v-row class="my-4">
                  <v-col cols="12" md="6" sm="12">
                    <AddressInfo :is-shipping="false" @address="updateAddress"  />
                  </v-col>
                  <v-col cols="12" md="6" sm="12">
                    <AddressInfo :is-shipping="true" @address="updateShipping" />
                  </v-col>
                </v-row>
            </v-form>
            </v-card-text>
            <v-card-actions class="my-5">
              <v-row justify="space-around" align-items="center">
                <v-btn color="primary" @click="createCustomer">
                  <v-icon left> mdi-account</v-icon>
                  Create Customer
                </v-btn>
                <v-btn v-if="hasCustomer" icon @click="show = !show" >
                  <v-icon>{{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
                </v-btn>
              </v-row>
            </v-card-actions>
            <v-expand-transition>
              <div v-show="show">
                <v-divider></v-divider>
                <v-card-text>
                  <pre >{{ customer }}</pre>
                </v-card-text>
              </div>
            </v-expand-transition>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card>

</template>

<script>
import AddressInfo from './AddressInfo.vue';

export default {
  components: { AddressInfo },
  data: () => ({
      mkey: '',
      mvalue: '',
      customer_data: {
          name: null,
          email: null,
          coupon: null,
          shipping: null,
          address: null,
          payment_method: null,
          test_clock: null,
          metadata: {}
      },
      customer: null,
      show: false
  }),
  computed: {
    hasCustomer() {
      return this.customer !== null
    }
  },
  methods : {
    updateAddress(address) {
      this.customer_data.address = address
    },
    updateShipping(address){
      this.customer_data.shipping = address
    },
    async createCustomer() {
      const {customer} = await this.$axios.$post('/customers/', this.customer_data);
      this.customer = customer
      this.$emit('customer-created', this.customer)
    },
    append_key_value() {
      this.customer_data.metadata[this.mkey] = this.mvalue
    }
  }
}
</script>

