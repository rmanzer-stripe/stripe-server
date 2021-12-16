
var clientSecret = ''



const getForm = () => {
    const id = document.getElementById('element-choice').value
    const response = `#${id}`
    return response
}
const getCustomer = () => {
    const custId = document.getElementById('customer').value;
    let name = null
    if (custId) {
        name = document.querySelector(`option[value=${custId}]`).textContent
    }
    return {id: custId, name}
}

const makeElements = (formId) => {
    showHideForm(formId);
    const useCard = formId.includes('card')
    const elementToCreate = useCard ? 'card' : 'payment'
    const options = useCard ? null : {clientSecret};
    const elements = stripe.elements(options);
    const myElement = elements.create(elementToCreate)
    myElement.mount(`#${elementToCreate}-element`)
    const retunrVal = useCard ? myElement : elements
    return retunrVal     
}

const handlePayment = (formToShow) => {
    const elements = makeElements(formToShow);
    document.querySelector(formToShow).addEventListener('submit', async (ev) =>{
        ev.preventDefault();
        const {error} = await stripe.confirmPayment({
            elements,
            confirmParams: {
                return_url: window.location.origin + "/success/",
            }
        })
        if (error) {
            errorMessageHandler(error.message)
        } else {
            errorMessageHandler('')
        }
    });
}

const handleCard = (formToShow) => {
    const elements = makeElements(formToShow);
    elements.on('change', (event) => {
        if (event.error) {
                errorMessageHandler(event.error.message);
        } else {
            errorMessageHandler('');
        }
    });
    document.querySelector(formToShow).addEventListener('submit', async (ev) => {
        ev.preventDefault();
        const customer = getCustomer();
        const {error} = await stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: elements,
                billing_details: {
                    name: customer.name
                },
            },
            return_url: window.location.origin + "/success/",
        })
        if (error) {
            errorMessageHandler(error.message)
        } else {
            errorMessageHandler('')
        }
    })
}

const paymentInit = (data) => {
    const formToShow = getForm();
    
    // Initialize stripe with public key
    stripeInit().then(() => {
        // const options = {
        //     clientSecret,
        //     appearance: {theme: 'night', labels: 'floating'}
        // }
        // showHideForm(formToShow);
        // const elements = stripe.elements(options);
        // const paymentElement = elements.create('payment');
        // paymentElement.mount('#payment-element');
        
        const confirmFunction = formToShow.includes('card') ? handleCard : handlePayment
        confirmFunction(formToShow)
        
    })
}

// Add initial for listener
document.querySelector('form#checkout-form').addEventListener('submit', async (ev) => {
    ev.preventDefault();
    let form = ev.target;
    let data = new FormData(form);
    let url = window.location.href
    const response = await fetch(
        url, {
            method: form.method,
            body: data
        }
    ).then(response => response.json())
    const stripe_data = response
    clientSecret = stripe_data.client_secret
    paymentInit(stripe_data)


})

