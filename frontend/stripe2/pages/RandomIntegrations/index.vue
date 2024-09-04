<template>
  <v-container>
  <v-row justify="center">
    <v-col cols="12" sm="8" offset-sm="2">
      <p class="text-h2">Random Integrations</p>
      <v-divider></v-divider>
      <p class="text-h5">Check them out. I think they're gonna be cool</p>
    </v-col>
    </v-row>
    <v-row class="mx-6">
      <v-col v-for="link in links" :key="link.title" cols="12" sm="3">
        <v-btn nuxt width="100%" color="indigo" outlined :to="link.to" elevation="3" class="white--text" @click="emitTitle(link.title)">{{ link.title }}</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "RandomIntegrationNavigation",
  computed: {
    links() {
      return this.$store.state.extra_nav_links
    }
  }, mounted() {
    this.$emit('update:title', null)
  },
  methods: {
    emitTitle(title){
      this.$emit('update:title', title)
    }
  },

}
</script>

<style>

</style>
