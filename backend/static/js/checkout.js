// Defining PaymentIntent UPE checkout methods

const form = document.getElementById('payment-form');

const options = {
    clientSecret: form.dataset.secret,
    appearance: {theme: 'night', labels: 'floating'}
}

fetch('/config/').then(response => response.json()).then((data) => {
    var stripe = Stripe(data.publicKey)
    const elements = stripe.elements(options)
    const payOptions = {fields: { billingDetails: {email: 'never'}}}
    const paymentElement = elements.create('payment', payOptions);
    paymentElement.mount('#payment-element');


    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const email = '';
        const {error} = await stripe.confirmPayment({
            elements,
            confirmParams: {
                return_url: 'http://localhost:8000/success',
                payment_method_data: { billing_details: { email } }
            },
        });

        if (error) {
            const messsageContainer = document.querySelector('#error-message');
            messsageContainer.textContent = error.message;
            messsageContainer.style.display = "block";
        } else {
            M.toast({html: 'Success'})
        }
    })
})