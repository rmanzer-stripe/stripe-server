
var clientSecret = ''

const showHideForm = (id) => {
    const formToShow = document.querySelector(id);
    const formsToHide = document.querySelectorAll(`form:not(${id})`)
    const btn = document.querySelector('button')
    btn.setAttribute('form', id.slice(1))
    if (id.includes('payment')){
        btn.textContent = 'Provide Payment Info'
    } else if (id.includes('card')){
        btn.textContent = 'Provide Card Info'
    } 
    else {
        btn.textContent = 'Register Subscription'
    }
    formsToHide.forEach(f => f.style.display = 'none');
    formToShow.style.display = 'block';
}

const getForm = () => {
    const id = document.getElementById('element-choice').value
    const response = `#${id}`
    return response
}

const makeElements = (formId) => {
    showHideForm(formId);
    const useCard = formId.includes('card')
    const elementToCreate = useCard ? 'card' : 'payment'
    const elements = stripe.elements({clientSecret})
    const myElement = elements.create(elementToCreate)
    myElement.mount(`#${elementToCreate}-element`)
    const retunrVal = useCard ? myElement : elements
    return retunrVal     
}

const handlePayment = (formToShow) => {
    const elements = makeElements(formToShow);
    document.querySelector(formToShow).addEventListener('sumibt', async (ev) =>{
        ev.preventDefault();
        return await stripe.confirmPayment({
            elements,
            confirmParams: {
                return_url: window.location.origin + "/success/",
            }
        })
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
        return await stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: elements,
                billing_details: {
                    name: ''
                }
            }
        })
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
        const {error} = confirmFunction(formToShow)
        
        if (error) {
            errorMessageHandler(error.message)
        } else {
            errorMessageHandler('')
        }
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

