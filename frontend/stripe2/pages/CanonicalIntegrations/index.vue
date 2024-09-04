<template>
  <v-row justify="center">
    <v-col v-for="link in links" :key="link.title" cols="12" lg="3" md="6" sm="12">
      <v-card :to="link.to" nuxt>
        <v-card-title >{{ link.title }}</v-card-title>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "CanonicalIntegrationsNav",
  computed: {
    links() {
      return this.$store.state.extra_nav_links
    }
  },
}
</script>

