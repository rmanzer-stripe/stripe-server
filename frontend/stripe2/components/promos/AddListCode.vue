<template>
  <v-row>
    <v-col cols="12" sm="12">
      <add-promo-code class="my-1" @promo-applied="addCode" />
    </v-col>
    <v-col cols="12" sm="12">
      <list-promo-codes :discounts="applied_codes" @removePromo="removeCode" />
    </v-col>
  </v-row>
</template>

<script>
import AddPromoCode from './AddPromoCode.vue'
import ListPromoCodes from './ListPromoCodes.vue'
export default {
  components: { AddPromoCode, ListPromoCodes },
  data: () => ({
    applied_codes: []
  }),
  methods: {
    addCode(code) {
      this.applied_codes.push(code)
    },
    removeCode(code) {
      this.applied_codes = this.applied_codes.filter(v => v !== code)
    }
  }
}
</script>
