<template>
  <v-card max-height="" flat>
    <v-card-title>Stripe Object {{ subtitle }}</v-card-title>
    <v-card-text class="py-4">
      <pre >{{stripeObject}}</pre>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    stripeObject: {type: [Object, Array], required: false, default: () => {}}
  },
  computed: {
    subtitle() {
      if(this.stripeObject){
        if (this.stripeObject.object) {
          return ` - ${this.stripeObject.object}`
        } else {
          return ""
        }
      } else {
        return ""
      }
    }
  }
}

</script>

<style scoped>
pre {
  border: 2px black;
  background-color: #123236;
  color: greenyellow;
  overflow: scroll;
}

</style>
