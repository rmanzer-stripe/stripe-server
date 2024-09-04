<template>
  <v-form class="pa-2">
    <v-row>
      <p>{{ title }}</p>
    </v-row>
    <v-row v-if="isShipping">
      <v-col cols="12" sm="6">
        <v-text-field v-model="name" label="Name" required></v-text-field>
      </v-col>
      <v-col cols="12" sm="6">
        <v-text-field v-model="phone" label="Phone"></v-text-field>
      </v-col>
    </v-row>
    <v-row v-else class="my-12"></v-row>
    <v-text-field v-model="address.line1" label="Line 1"></v-text-field>
      <v-text-field v-model="address.line2" label="Line 2"></v-text-field>
    <v-row>
        <v-col cols="12" md="8" sm="12">
          <v-text-field v-model="address.city" label="City"></v-text-field>
        </v-col>
        <v-col cols="12" md="4" sm="12">
          <v-select v-model="address.state" :items="stateItems" item-text="state" item-value="abbr" label="State"></v-select>
        </v-col>
        <v-col cols="12" sm="12" md="6">
          <v-text-field v-model="address.postal_code" label="Postal Code"></v-text-field>
        </v-col>

    </v-row>
  </v-form>
</template>

<script>
export default {
  props: {
    isShipping: {type: Boolean, required: false, default: false}
  },
  data: () => ({
    address: {
      city: null,
      country: 'US',
      line1: null,
      line2: null,
      state: null,
      postal_code: null,
    },
    name: null,
    phone: null,
    states : [
        ['Arizona', 'AZ'],
        ['Alabama', 'AL'],
        ['Alaska', 'AK'],
        ['Arkansas', 'AR'],
        ['California', 'CA'],
        ['Colorado', 'CO'],
        ['Connecticut', 'CT'],
        ['Delaware', 'DE'],
        ['Florida', 'FL'],
        ['Georgia', 'GA'],
        ['Hawaii', 'HI'],
        ['Idaho', 'ID'],
        ['Illinois', 'IL'],
        ['Indiana', 'IN'],
        ['Iowa', 'IA'],
        ['Kansas', 'KS'],
        ['Kentucky', 'KY'],
        ['Louisiana', 'LA'],
        ['Maine', 'ME'],
        ['Maryland', 'MD'],
        ['Massachusetts', 'MA'],
        ['Michigan', 'MI'],
        ['Minnesota', 'MN'],
        ['Mississippi', 'MS'],
        ['Missouri', 'MO'],
        ['Montana', 'MT'],
        ['Nebraska', 'NE'],
        ['Nevada', 'NV'],
        ['New Hampshire', 'NH'],
        ['New Jersey', 'NJ'],
        ['New Mexico', 'NM'],
        ['New York', 'NY'],
        ['North Carolina', 'NC'],
        ['North Dakota', 'ND'],
        ['Ohio', 'OH'],
        ['Oklahoma', 'OK'],
        ['Oregon', 'OR'],
        ['Pennsylvania', 'PA'],
        ['Rhode Island', 'RI'],
        ['South Carolina', 'SC'],
        ['South Dakota', 'SD'],
        ['Tennessee', 'TN'],
        ['Texas', 'TX'],
        ['Utah', 'UT'],
        ['Vermont', 'VT'],
        ['Virginia', 'VA'],
        ['Washington', 'WA'],
        ['West Virginia', 'WV'],
        ['Wisconsin', 'WI'],
        ['Wyoming', 'WY'],
    ]
  }),
  computed: {
    addressValue() {
      let obj = {}
      if (this.isShipping) {
        obj = {name: this.name, phone: this.phone, address: this.address}
      } else {
        obj = this.address
      }
      return obj
    },
    stateItems() {
      return this.states.map(state => {return {abbr: state[1], state: state[0]}} )
    },
    title() {
      return this.isShipping ? 'Shipping Address' : 'Address';
    }
  },
  methods: {
    emitAddress() {
      this.emit('address', this.addressValue)
    }
  }
}
</script>
