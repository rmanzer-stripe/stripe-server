import colors from 'vuetify/es5/util/colors'

export default {
  // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
  ssr: false,

  // Target: https://go.nuxtjs.dev/config-target
  target: 'static',

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    titleTemplate: '%s - Supermanzer',
    title: 'Supermanzer',
    htmlAttrs: {
      lang: 'en',
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' },
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
    script: [
      { src: 'https://js.stripe.com/v3' },
      { src: 'https://js.stripe.com/terminal/v1/' },
      { src: 'https://js.stripe.com/v3/pricing-table.js' },
      { src: 'https://connect-js.stripe.com/v1.0/connect.js' },
    ],
  },

  env: {
    STRIPE_PK:
      'pk_test_51JticYIlCeH6bP8REulC9GlUO09hWuGsCljwJ3VNWhqqLmTTW0CedWXOoABWyXkplmqMtwfA4SiXkdeqCMvesIii00BCpJb9Vb',
    ACCOUNTS: [
      { id: 'acct_1JticYIlCeH6bP8R', name: 'rmanzer+test@stripe.com'},
      { id : 'acct_1K9BjQKyzYDRNndd', name: 'Supermanzer Software Consulting'},
      { id: 'acct_1O83hCB9iVsTMEuJ', name: 'British Manzer'},
      { id: 'acct_1MDBBRJCMaYNrHEB', name: 'Emirate Wombats'},
      { id: 'acct_1PMeTpL3oXCU477z', name: 'French Manzer'}
    ]
  },
  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    { src: '~/plugins/vue-stripe.js', ssr: false },
    { src: '~/plugins/formatting.js', ssr: false },
    { src: '~/plugins/axios.js', ssr: false },
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/eslint
    '@nuxtjs/eslint-module',
    // https://go.nuxtjs.dev/vuetify
    '@nuxtjs/vuetify',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    // https://go.nuxtjs.dev/content
    '@nuxt/content',
    // Stripe Connect module
    // '@stripe/connect-js'
  ],

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    // Workaround to avoid enforcing hard-coded localhost:3000: https://github.com/nuxt-community/axios-module/issues/308
    // baseURL: 'https://rmanzer-api.tunnel.stripe.me/api/',
    // baseURL: 'http://localhost:8000/api/',
  },
  server: {
    port: 3000, // default: 3000
    // host: '0.0.0.0', // default: localhost,
    // timing: false
  },

  // Content module configuration: https://go.nuxtjs.dev/config-content
  content: {},

  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      dark: false,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3,
        },
      },
    },
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    // transpile:['@stripe/connect-js']
  },
  router: {
    extendRoutes(routes, resolve) {
      routes.push({
        name: 'apple-pay',
        path: '.well-known/apple-developer-merchantid-domain-association',
        component: resolve(__dirname, 'pages/treasury.vue'),
        })
    },
  }
}
