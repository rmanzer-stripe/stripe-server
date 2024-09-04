<template>
  <v-alert
    :border="border"
    colored-border
    :type="alertType"
    elevation="2"
    dismissible
  >
    {{message}}
  </v-alert>
</template>

<script>
export default {
  name: 'CoreAlert',
  props: {
    border: {
      type: String,
      required: false,
      default: "left"
    },
    alertType: {
      type: String,
      required: false,
      default: "warning"
    },
    message: {
      type: String,
      required: false,
      default: "Something has occurred"
    }
  }
}
</script>

<style>

</style>
