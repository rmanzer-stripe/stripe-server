<template>
  <v-select
    v-model="mode"
    :items="modes"
    label="Select Mode"
    hint="Set the mode for Stripe.js elements"
    @change="emitMode"
  ></v-select>
</template>

<script>
export default {
  props: {
    modes: {type: Array, required: false, default: () => ['payment', 'setup', 'subscription']},
    default: {type: String, required: false, default: 'payment'}
  },
  data: () => ({
    mode: null
  }),
  created() {
    this.mode = this.default
  },
  methods: {
    emitMode() {
      this.$emit('mode', this.mode)
    }
  }
}
</script>
