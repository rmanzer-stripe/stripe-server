export default ({ app }, inject) => {
  inject('format',{
    stripePrice(amount) {
      if (amount === 0) {
        return '$0.00'
      }
      else if (amount) {
        const float = amount / 100
        return `$${float.toFixed(2)}`
      } else {
        return ''
      }
    },
    convertTimestamp(timestamp) {
      if (timestamp) {
        const date = new Date(timestamp*1000)
        return date.toLocaleString('en-US', { timeZone: 'UTC' })
      } else {
        return ''
      }
    }
  })
}
