/*
 * JavaScript functionality for older subscription flow documented here
 *  https://stripe.com/docs/billing/subscriptions/fixed-price
 */

const createCustomer = async (ev) => {
    let form = ev.target;
    let data = new FormData(form);
    const response = await fetch('/create-customer', {
        method: 'POST',
        body: data
    })
    return response.json()
}   

const handleCard = () => {
    const elements = stripe.elements();
    const card = elements.create('card')
    card.mount('#card-element');
    card.on('change', (event) => {
        if (event.error) {
                errorMessageHandler(event.error.message);
        } else {
            errorMessageHandler('');
        }
    });
    return card
}

const createPaymentMethod = (card) => {
    const customerId = document.getElementById('customerId').value;
    const billingName = document.querySelector('#full-name').value;
    const form = new FormData(document.getElementById('payment-form'))
    const priceId = form.get('price');
    stripe.createPaymentMethod({
        type: 'card',
        card: card,
        billing_details: {
            name: billingName,
        },
    }).then((result) => {
        if (result.error) {
            console.log(result.error);
            errorMessageHandler(result.error.message)
        } else {
            // TODO: Stay on this
            // More stuff goes here
            // https://stripe.com/docs/billing/subscriptions/fixed-price#create-subscription
        }
    })
    
}
stripeInit().then(() => {
    document.querySelectorAll('label.card-radio').forEach(el => {
        el.addEventListener('click', (ev) => {
            if (ev.target.tagName == 'INPUT') {
                // WE only take action on the input click event
                const target = ev.target;
                const inputs = ev.target.closest('form').querySelectorAll('input[type="radio"');
                inputs.forEach(element => {
                    if (element === target) {
                        element.nextElementSibling.classList.add('active')
                        element.checked = true
                    } else {
                        element.nextElementSibling.classList.remove('active')
                        element.checked = false
                    }
                })
            }
        })
    })

    document.querySelector('form#customer').addEventListener('submit', async (ev) => {
        ev.preventDefault();
        const customer = await createCustomer(ev);
        document.getElementById('customerId').value = customer.id;
        showHideForm('#payment-form');
        const card = handleCard();
        document.querySelector('form#payment-form').addEventListener('submit', (event) => {
            event.preventDefault();
            createPaymentMethod(card);
        })
    })
})




