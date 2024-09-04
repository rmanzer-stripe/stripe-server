<template>
  <v-list>

    <component :is="linkComponent(link)" v-for="(link, i) in links" :key="i" :link="link" :mini="mini" />
  </v-list>
</template>

<script>
import ChildrenLinks from '~/components/nav/ChildrenLinks.vue'
import SimpleLink from '~/components/nav/SimpleLink.vue'

export default {
  props: {
    links: {type: Array, required: false, default: () => []},
    mini: {type: Boolean, required: false, default: false},
  },
  methods: {
    linkComponent(link) {
      return Object.prototype.hasOwnProperty.call(link, 'children') ? ChildrenLinks : SimpleLink
    }
  }
}
</script>

