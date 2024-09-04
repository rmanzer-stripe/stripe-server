<template>
  <v-container fluid class="white pa-8">
    <nuxt-child/>
  </v-container>
</template>

<script>

export default {
  name: 'OrdersAPI',

  computed: {
    has_status() {
      return Object.keys(this.$route.query).includes('redirect_status')
    }
  }

}
</script>

