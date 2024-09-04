<template>
  <v-text-field v-model="value" type="number" :rules="rules" :label="label" :hint="hint"></v-text-field>
</template>

<script>
export default {
  name: "IntegerInput",
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
