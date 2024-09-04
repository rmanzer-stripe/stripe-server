<template>
  <v-alert border="top" colored-border :type="readerStatus.type" elevation="2">
    {{readerStatus.message}}
  </v-alert>
</template>

<script>

export default {
  props: {
      readerId: {type: String, required: false, default: null}
  },
  data: () => ({
    reader: null,
    interval: null,
  }),
  computed: {
    readerStatus() {
      // TODO: Create a specific status based on the reader prop - both alert type and message
      const status = { type: 'info', message: '' };
      if (this.reader === null || this.reader.deleted === true ) {
        status.type = 'warning'
        status.message = 'No reader connected'
      } else {
        const reader_status = this.reader.action !== null ? this.reader.action.status : this.reader.status
        switch (reader_status) {
          case 'in_progress':
            status.type = 'warning'
            status.message = 'Reader processing'
            break;
          case 'failed':
            status.type = 'error'
            status.message = 'Payment confirmation failed'
            break;
          case 'succeeded':
            status.type = 'success'
            status.message = 'Payment confirmation succeeded'
            break;
          case 'offline':
            status.type = 'warning'
            status.message = 'Reader offline'
            break;
          default:
            status.type = 'info'
            status.message = 'Reader ready'
            break;
        }
      }
      return status
    }
  },
  mounted() {
    this.interval = setInterval(() => {this.pollReader()}, 5000)
  },
  destroyed() {
    console.log("clearing the inverval");
    const interval = this.interval
    clearInterval(interval)
  },
  methods: {
    async pollReader() {
      if (this.readerId !== null) {
        const url = `/terminals/${this.readerId}/reader_status/`
        this.reader = await this.$axios.$get(url)
        if (this.reader.action !== null && this.reader.action.status === "succeeded") {
          this.$emit("success")
        }
      }
    }
  },

}
</script>
