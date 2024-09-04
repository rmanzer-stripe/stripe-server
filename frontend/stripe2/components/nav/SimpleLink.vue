
<template>
  <v-list-item :to="link.to" router exact>
    <v-tooltip v-if="mini" right>
      <template v-slot:activator="{on, attrs}">
        <v-list-item-icon>
          <v-icon v-bind="attrs" v-on="on">{{ link.icon }}</v-icon>
        </v-list-item-icon>
      </template>
      <span>{{ link.title }}</span>
    </v-tooltip>
    <v-list-item-icon v-else>
      <v-icon>{{ link.icon }}</v-icon>
    </v-list-item-icon>
    <v-list-item-content>
      <v-list-item-title v-text="link.title" />
    </v-list-item-content>
    <v-list-item-icon v-if="deprecated">
      <v-tooltip left>
        <template v-slot:activator="{on, attrs}">
          <v-icon color="orange" v-bind="attrs" v-on="on">mdi-alert-outline</v-icon>
        </template>
        <span>Integration Deprecated</span>
      </v-tooltip>
    </v-list-item-icon>
  </v-list-item>
</template>

<script>
export default {
  name:'NavLink',
  props: {
    link: {type: Object, required: true},
    mini: {type: Boolean, required: false, default: false}
  },

  computed: {
    deprecated() {
      // eslint-disable-next-line no-prototype-builtins
      if (this.link.hasOwnProperty('deprecated') && this.link.deprecated === true) {
        return true
      }
      return false
    }
  }
}
</script>
