// General purpose Javascript Functions

// Centralizing the definitions of url endpoints to make mainteance easier
const appUrls = {
    config: '/config/',
    checkoutSession: '/create-checkout-session/',
}

// Ensuring the Stripe
var stripe = {}


// Initializing Stripe.js on the home page when the page loads with the public key
fetch(appUrls.config).then((result) => result.json()).then((data) => {
   stripe = Stripe(data.publicKey)
})

// Binding an event to the button on the homepage
document.querySelector('#submitBtn').addEventListener('click', () => {
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


