<template>
  <pre class="code" v-if="hasObject" he>
    {{ object }}
  </pre>
</template>

<script>
export default {
  props: {
    object: {type: Object, required: false, default: () => {}}
  },
  computed: {
    hasObject() {
      if (this.object !== null) {
        return Object.keys(this.object).length > 0
      } else {
        return false
      }
    }
  }
}
</script>

<style>
pre {
  border: 2px black;
  background-color: #123236;
  color: greenyellow;
  overflow-x: auto;
  max-height: 800px;
}
</style>
