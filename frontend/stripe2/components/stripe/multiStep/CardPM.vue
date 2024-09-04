<template>

  <v-list two-line>
    <v-list-item v-for="field in displayFields" :key="field.name">
      <v-list-item-content>
        <v-list-item-title v-text="field.name"></v-list-item-title>
        <v-list-item-subtitle v-text="field.value"></v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>
  </v-list>

</template>

<script>
export default {
  props: {
    card: {type: Object, required: false, default: () => {}}
  },
  computed: {
    displayFields() {
      return [
        {
          name: 'Card brand',
          value: this.card.display_brand
        },
        {
          name: 'Card funding',
          value: this.card.funding
        },
        {
          name: 'Last 4 digits',
          value: this.card.last4
        },
        {
          name: 'Expiration',
          value: `${this.card.exp_month}/${this.card.exp_year}`
        }
      ]
    }
  }
}
</script>

<style>

</style>
