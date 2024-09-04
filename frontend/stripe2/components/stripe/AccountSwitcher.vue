<template>
  <v-select
    v-model="selected"
    hint="Choose an account to make API requests for"
    :items="accounts"
    item-text="name"
    item-value="id"
    persistent-hint
    single-line
    return-object
    @change="setAccount"
  ></v-select>
</template>

<script>
import { mapMutations} from 'vuex'
export default {
  data: () => ({
    accounts: [],
    selected: null
  }),
  created() {
    this.selected = this.$store.state.account
    this.accounts = this.$store.state.accounts
  },
  methods: {
   ...mapMutations({
    setAccount: 'setAccount'
   }),
  }
}
</script>


