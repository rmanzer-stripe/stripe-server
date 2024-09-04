
export default function ({ $store, $axios, app }) {
  if (process.client) {
    const host = window.location.host;
    if (host.includes('localhost')) {
      $axios.defaults.baseURL = 'http://localhost:8000/api/';
    } else {
      $axios.defaults.baseURL = "https://rmanzer-api.tunnel.stripe.me/api/";
    }
  }
}
