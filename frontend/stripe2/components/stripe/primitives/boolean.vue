<template>
  <v-switch :label="label" :hint="hint" :rules="rules" :color="color" :value="fieldValue" @change="$emit('update:fieldValue', $event)"></v-switch>
</template>

<script>
export default {
  name: 'BooleanInput',
  props: {
    rules: {type: Array, required: false, default: () => []},
    label: {type: String, required: false, default: ''},
    hint: {type: String, required: false, default: null},
    color: {type: String, required: false, default: 'primary'},
    fieldValue: {type: Boolean}
  },
  emits: ['myTruth'],
  methods: {
    sendEvent(val) {
      this.$emit('myTruth', val)
    }
  }
}
</script>
