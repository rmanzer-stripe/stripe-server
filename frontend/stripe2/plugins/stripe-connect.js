import { loadConnect } from "@stripe/connect-js"

export default ({ app }, inject) => {
  inject('stripeConnect',  () => {
    return loadConnect()
  })
}
