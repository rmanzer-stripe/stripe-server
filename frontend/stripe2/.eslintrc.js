module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
  },
  parserOptions: {
    parser: '@babel/eslint-parser',
    requireConfigFile: false,
  },
  extends: [
    '@nuxtjs',
    'plugin:nuxt/recommended',
    'prettier',
    'plugin:vuetify/base',
  ],
  plugins: [],
  // add your custom rules here
  rules: {
    'vue/camelcase': 0,
    camelcase: 0,
    'no-console': 'off',
  },
}
