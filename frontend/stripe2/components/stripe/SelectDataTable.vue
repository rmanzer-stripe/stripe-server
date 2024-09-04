<template>
  <v-data-table
    v-model="selected"
    show-select
    :items="items"
    :headers="headers"
    :single-select="singleSelect"
  ></v-data-table>
</template>

<script>
export default {
  props: {
    items: {type: Array, required: false, default: () => []},
    headers: {type: Array, required: false, default: () => []},
    singleSelect: {type: Boolean, required: false, default: false},
    loading: {type: Boolean, required: false, default: false}
  },
  data: () => ({
    selected: []
  }),
  watch: {
    selected() {
      this.emitSelected()
    }
  },
  methods: {
    emitSelected(){
      this.$emit('selected', this.selected)
    }
  },

}
</script>
