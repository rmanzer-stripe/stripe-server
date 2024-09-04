export const state = () => ({
  customer: null,
  extra_nav_links: null,
  account: {
    id: 'acct_1JticYIlCeH6bP8R',
    name: 'Default Acct',
    pk: 'pk_test_51JticYIlCeH6bP8REulC9GlUO09hWuGsCljwJ3VNWhqqLmTTW0CedWXOoABWyXkplmqMtwfA4SiXkdeqCMvesIii00BCpJb9Vb'
  },
  accounts: [
    {
      id: 'acct_1JticYIlCeH6bP8R',
      name: 'Default Acct',
      pk: 'pk_test_51JticYIlCeH6bP8REulC9GlUO09hWuGsCljwJ3VNWhqqLmTTW0CedWXOoABWyXkplmqMtwfA4SiXkdeqCMvesIii00BCpJb9Vb'
    },
    {
      id: 'acct_1O83hCB9iVsTMEuJ',
      name: 'British Manzer',
      pk: 'pk_test_51O83hCB9iVsTMEuJAZG1sXHvTEocuvmdoy1i6cRTEBpHPuNkgnr6PS0Dgn5QceFfmqfbxgwvJdSyxj80TfiLcSbN00rFGUFO04'
    },
    {
      id: 'acct_1PMeTpL3oXCU477z',
      name: 'French Manzer',
      pk: 'pk_test_51PMeTpL3oXCU477zrDSUdVm1P9AEW8mtswwnFEl6iAUfzg0g0fapz1iL9o4gq2tXAnrxG3taUiZppE5hEnQoqbMl00bX3RjzwD'
    },
    {
      id: 'acct_1Ppek1Q6JWPgQcCn',
      name: 'Sandbox 1 - Stock Shop',
      pk: 'pk_test_51Ppek1Q6JWPgQcCnLiLPZFAfxocDEirCX1SEJcgo1QEqiVfVaqslX5vnmqGUTvXigZWi6G5ccfSEFrbIpv4i0JT000o2z9nr5T'
    },
    {
      id: 'acct_1PnNzpIWHOnXaRR4',
      name: 'Sandbox 2 - Default Account',
      pk: 'pk_test_51PnNzpIWHOnXaRR4NBLSkFknlPbl2KnFmIoVpaVy3zq0ZxWIPOfQm596QqWcO0JQ5zqj2hRXSulpec2srolZG3Eb00dFZPSKUj'
    }
  ],
  stripeObjects: {}
})

export const getter = {
  getCustomer(state) {
    return state.customer
  },
  getNavLinks(state) {
    return state.extra_nav_links
  },
  getAccount(state) {
    return state.account
  }
}

export const mutations = {
  setCustomer(state, customer) {
    state.customer = customer
  },
  setNavLinks(state, navLinks) {
    state.extra_nav_links = navLinks
  },
  setAccount(state, account) {
    state.account = account
  },
  updateStripeObject(state, { key, value }) {
    state.stripeObjects[key] = value
  },
  clearStripeObjects(state) {
    state.stripeObjects = {}
  }
}
