<template>
  <v-list-group :value="false" :prepend-icon="link.icon">
    <template v-slot:activator>
      <v-list-item-content>
        <v-list-item-title>
          {{link.title}}
        </v-list-item-title>
      </v-list-item-content>
    </template>
      <simple-link v-for="(child, index) in link.children" :key="index" :link="child" :mini="mini"/>
  </v-list-group>
</template>

<script>
import SimpleLink from './SimpleLink.vue'
export default {
  components: { SimpleLink },
  props: {
    link: {type: Object, required: true},
    mini: {type: Boolean, required: false, default: false}
  }
}
</script>
