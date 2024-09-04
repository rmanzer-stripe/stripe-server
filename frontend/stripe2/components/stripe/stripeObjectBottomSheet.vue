<template>
  <v-bottom-sheet

  ></v-bottom-sheet>
</template>

<script>
export default {
  props: {sheet: {type: Boolean, required: false, default: false}},
  computed: {
    objects() {
      return this.$store.state.stripeObjects
    }
  }
}
</script>

<style>

</style>
