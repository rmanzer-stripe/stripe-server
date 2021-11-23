// General purpose Javascript Functions

// Centralizing the definitions of url endpoints to make mainteance easier
const appUrls = {
    config: '/config/',
    checkoutSession: '/create-checkout-session/',
}

const preloader = `
    <div class="progress">
      <div class="indeterminate"></div>
  </div>
`

// Ensuring the Stripe
var stripe = {}


// Initializing Stripe.js on the home page when the page loads with the public key
function stripeInit() {
    return fetch(appUrls.config).then((result) => result.json()).then((data) => {
        stripe = Stripe(data.publicKey)
    })
}


// Binding an event to the button on the homepage
const el = document.querySelector('#checkoutBtn')
if (el) {
    el.addEventListener('click', () => {
        stripeInit();
        // Get Checkout Session ID
        fetch(appUrls.checkoutSession)
        .then(result => result.json())
        .then((data) => {
            console.log(data);

            return stripe.redirectToCheckout({sessionId: data.sessionId})
        })
        .then((res) => {
            console.log(res);
        })
    })    
}

function stripePaymentMethodHandler(result) {
    var token = document.querySelector('input[name=csrfmiddlewaretoken]').value
    const el = document.getElementById('card-errors');
    if (result.error) {
        
        el.classList.add('red', 'lighten-4', 'red-text', 'text-darken-4');
        el.innerHTML = result.error.message;
    } else {
        fetch('/pi-hold/', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRFToken': token
            },
            body: JSON.stringify({
                payment_method_id: result.paymentMethod.id,
            })
        }).then(function(result) {
            // Handle server response (see Step 4)
            result.json().then(function(json) {
                handleServerResponse(json);
            })
        }).catch(err => {
            el.classList.add('red', 'lighten-4', 'red-text', 'text-darken-4');
            el.innerHTML = err
        });
    }
}

function handleServerResponse(response) {
    console.log(response)
    const el = document.getElementById('card-errors');
    if (response.error) {
        el.innerHTML = response.error.message
        el.classList.add('red', 'lighten-4', 'red-text', 'text-darken-4');
    } else if (response.requires_action) {
        stripe.handleCardAction(
            response.payment_intent_client_secret
        ).then(handleStripeJsResult)
    } else {
        el.innerHTML = "Success! You gave us money!"
        el.classList.remove('red', 'lighten-4', 'red-text', 'text-darken-4');
        el.classList.add('green', 'lighten-4', 'green-text', 'text-darken-4');
    }
}

const messageModal = (message, heading='') => {
    const modal = document.getElementById('modal-1');
    const content = document.getElementById('modal-content');
    contentText = `
    <h3>${heading}</h3>
    <div class="divider"></div>
    <p>${message}</p>
    `;
    content.innerHTML = contentText;
    M.Modal.getInstance(modal).open();
}