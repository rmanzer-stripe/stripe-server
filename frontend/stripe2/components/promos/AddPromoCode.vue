<template>
  <v-row >

      <v-text-field
        v-model="code"
        label="Enter promo code"
        :append-outer-icon="hasCode ? 'mdi-plus-circle' : 'mdi-minus'"
        :rules="[v => applicable_codes.includes(v)]"
        :hint="`Promo code must be one of ${applicable_codes}`"
        persistent-hint
        @click:append-outer="emitCode"
      ></v-text-field>

  </v-row>
</template>

<script>
export default {
  data: () => ({
    code: '',
    applicable_codes: ['CADOS4LESS', 'TAKE10', 'SAVE50'],
  }),
  computed: {
    hasCode() {
      return this.code.length > 0
    }
  },
  methods: {
    emitCode() {
      if (this.hasCode) {
        this.$emit('promo-applied', this.code)
        this.code = ''
      }
    },
    checkCode() {
      // TODO: Implement some way to check if this code is valid before applying it
    }
  }
}
</script>
