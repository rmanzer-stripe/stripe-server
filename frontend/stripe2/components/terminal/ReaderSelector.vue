<template>
  <v-select
    v-model="reader"
    :items="readers"
    item-text="label"
    item-value="id"
    label="Select Reader"
    return-object
    @change="selectReader"
  ></v-select>
</template>

<script>
export default {
  props: {
    readers: {type: Array, required: false, default: () => []}
  },
  data: () => ({
    reader: null
  }),
  methods: {
    selectReader() {
      this.$emit("change", this.reader)
    }
  }
}
</script>
