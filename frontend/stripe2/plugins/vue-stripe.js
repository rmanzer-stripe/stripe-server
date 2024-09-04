import Vue from 'vue'
import { StripePlugin } from '@vue-stripe/vue-stripe'

const accounts = {
  acct_1JticYIlCeH6bP8R: 'pk_test_51JticYIlCeH6bP8REulC9GlUO09hWuGsCljwJ3VNWhqqLmTTW0CedWXOoABWyXkplmqMtwfA4SiXkdeqCMvesIii00BCpJb9Vb', // rmanzer+test#stripe.com
  acct_1O83hCB9iVsTMEuJ: 'pk_test_51O83hCB9iVsTMEuJAZG1sXHvTEocuvmdoy1i6cRTEBpHPuNkgnr6PS0Dgn5QceFfmqfbxgwvJdSyxj80TfiLcSbN00rFGUFO04', // British Manzer
  acct_1PMeTpL3oXCU477z: 'pk_test_51PMeTpL3oXCU477zrDSUdVm1P9AEW8mtswwnFEl6iAUfzg0g0fapz1iL9o4gq2tXAnrxG3taUiZppE5hEnQoqbMl00bX3RjzwD', // French Manzer
}

export default ({store}) => {
  const pk = accounts[store.state.account.id]
  const options = {
    pk
  }
  Vue.use(StripePlugin, options)
}
