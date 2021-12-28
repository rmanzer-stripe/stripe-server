

/**
 * Display error if exists, otherwise clear error div
 * @param {Object} error error object returned by Stripe API
 */
const errMessageHandler = (error) => {
    const errDiv = document.getElementById('error-message');
    if (error) {
        errDiv.textContent = error.message;    
        errDiv.style.display = 'block'
    } else {
        errDiv.textContent = ''
        errDiv.style.display = 'none'
    }
}


stripeInit().then(() => {
    const options = {
        clientSecret : document.getElementById('client-secret').value,
        appearance: {
            theme: 'night',
            labels: 'floating'
        },
    }
    
    const elements = stripe.elements(options);

    const paymentElement = elements.create('payment');
    paymentElement.mount('#payment-element')
    const form = document.getElementById('setup-form')
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const { error }= await stripe.confirmSetup({
            elements,
            confirmParams: {
                return_url: window.location.href
            }
        })
        errMessageHandler(error)
    })
})