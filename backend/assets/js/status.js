/**
 * Check status of payment intent and return values to the user
 */

stripeInit().then(() => {
    const clientSecret = new URLSearchParams(window.location.search).get(
        'payment_intent_client_secret'
    )
    if (clientSecret){
        stripe.retrievePaymentIntent(clientSecret).then(({paymentIntent}) => {
            const message = document.querySelector('#message')
            const alert = document.querySelector('#status-alert')
            switch (paymentIntent.status) {
                case 'succeeded':
                    message.textContent = 'Success! Payment Received'
                    alert.classList.add(['alert-success'])
                    break;
                case 'processing':
                    message.textContent = 'Payment is processing.  Stay tuned.....'
                    alert.classList.add(['alert-warning'])
                    break;
                case 'requires_payment_method':
                    message.textContent = 'Payment failed.  Please try another payment method';
                    // TODO: Figure out redirect without hardcoding URL
                    alert.classList.add(['alert-error'])
                    break;
                default:
                    message.textContent = "Something went wrong...."
                    alert.classList.add(['alert-error'])
                    break;
            }
        })
    }
    
})