<template>

  <v-list subheader>
    <v-subheader>Promo Codes Applied</v-subheader>
    <template v-for="discount in discounts">
      <v-list-item :key="discount">
        <v-list-item-content>
          <v-list-item-title v-text="discount"></v-list-item-title>
        </v-list-item-content>
        <v-list-item-action>
          <v-btn
            color="indigo"
            text
            @click="emitRemove(discount)"
          >REMOVE</v-btn>
        </v-list-item-action>
      </v-list-item>
    </template>
  </v-list>

</template>

<script>
export default {
  props: {
    discounts: {type: Array, required: false, default: () => []}
  },
  methods:{
    emitRemove(discount) {
      this.$emit("removePromo", discount)
    }
  }
}
</script>
