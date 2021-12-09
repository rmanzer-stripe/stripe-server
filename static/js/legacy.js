// static/js/legacy.js

const cardEventHandler = (event) => {
    const displayError = document.getElementById('card-errors');
    if (event.error) {
        displayError.textContent = event.error.message
        displayError.style.display = 'block';
    } else if (event.token) {
        document.getElementById('stripeToken').setAttribute('value', event.token.id);
        document.getElementById('paymentForm').submit();
    } else {
        displayError.textContent = '';
        displayError.style.display = 'none';
    }
}

// Initialing the Stripe library
stripeInit().then(() => {
    const elements = stripe.elements();
    const style = {
         base: {
            iconColor: '#29b6f6',
            color: '#0d47a1',
            fontWeight: '500',
            fontFamily: '"Raleway", "Lato", "Montserrat", sans-serif',
            fontSize: '16px',
            fontSmoothing: 'antialiased',
            ':-webkit-autofill': {
                color: '#fce883',
            },
            '::placeholder': {
                color: '#87BBFD',
            },
        },
        invalid: {
            iconColor: '#d50000',
            color: '#b71c1c',
        },
    };
    const card = elements.create('card', { style })
    card.mount('#payment-card')

    card.on('change', (event) => {
        cardEventHandler(event)
    });
    const form = document.getElementById('paymentForm')
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        let details = {
            name: document.getElementById('cardholderName').value,
        }
        const fields = ['address_line1', 'address_line2', 'address_city', 'address_state', 'address_zip']
        fields.forEach(el => {
            details[el] = document.getElementById(el).value
        })
        console.log(details);
        stripe.createToken(card, details).then(cardEventHandler);
    })
})