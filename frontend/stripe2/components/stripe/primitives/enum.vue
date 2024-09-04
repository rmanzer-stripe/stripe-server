<template>
  <v-select v-model="value" :items="items" :label="label" :hint="hint" :rules="rules" ></v-select>
</template>
<script>
export default {
  name: "EnumInput",
  props: {
    rules: {type: Array, required: false, default: () => []},
    label: {type: String, required: false, default: ''},
    hint: {type: String, required: false, default: null},
    items: {type: Array, required:true}
  },
  data: () => ({
    value: null
  }),
}
</script>
