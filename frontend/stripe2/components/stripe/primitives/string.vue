<template>
  <v-text-field
  v-model="value"
    type="text"
    :rules="rules"
    :label="label"
    :hint="hint"
  >

  </v-text-field>
</template>

<script>
export default {
  name: "StringField",
  props: {
    rules: {type: Array, required: false, default: () => []},
    label: {type: String, required: false, default: ''},
    hint: {type: String, required: false, default: null}
  },
  data: () => ({
    value: null
  })
}
</script>
