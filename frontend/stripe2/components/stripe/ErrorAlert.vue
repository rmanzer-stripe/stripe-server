<template>
  <v-alert v-if="error" type="error" border="left" colored-border elevation="3" dismissible @click="emitDismiss">
    <p class="text-h5">Error</p>
    <p class="text-h6">Code: {{ error.code }}</p>
    <p class="">Type: {{ error.type }}</p>
    <p class="">Request: {{ error.request_log_url }}</p>
    <v-divider></v-divider>
    <p>Message: <pre>{{ error.message }}</pre></p>
  </v-alert>
</template>

<script>
export default {
  props: {
    error: {type: Object, required: false, default: () => {}}
  },
  methods: {
    emitDismiss() {
      this.$emit('dismissed')
    }
  }
}
</script>
