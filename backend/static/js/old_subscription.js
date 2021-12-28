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
    const style = {
      base: {
        color: "#32325d",
        fontFamily: 'Arial, sans-serif',
        fontSmoothing: "antialiased",
        fontSize: "16px",
        "::placeholder": {
          color: "#32325d"
        }
      },
      invalid: {
        fontFamily: 'Arial, sans-serif',
        color: "#fa755a",
        iconColor: "#fa755a"
      }
    };
    const card = elements.create('card', {style})
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

const onSubscriptionComplete = (result) => {
    if (result.subscription.status === 'active') {
       const forms =  document.querySelectorAll('form')
        for (let i = 0; i < forms.length; i++) {
            const form = forms[i];
            form.style.display = 'none';
        }
        const successDiv = document.getElementById('success-message');
        successDiv.textContent = "You have been successfully subscribed!"
        successDiv.style.display = 'block';
        document.getElementById('submit-btn').style.display = 'none'
        document.getElementById('home-btn').style.display = 'block'
    }
}

const handlePaymentRequiringCustomerAction = ({subscription, invoice, priceId, paymentMethodId, isRetry}) => {
    if (subscription && subscription.status === 'active') {
        return {subscription, priceId, paymentMethodId};
    }
    let paymentIntent = invoice ? invoice.payment_intent : subscription.latest_invoice.payment_intent;
    if (
        paymentIntent.status === 'requires_action' ||
        (isRetry === true && paymentIntent.status === 'requires_payment_method')
    ) {
        return stripe.confirmCardPayment(paymentIntent.client_secret, {payment_method: paymentMethodId})
        .then((result) => {
            if (result.error) {
                throw result;
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    M.toast('Success')
                    return {
                        priceId,
                        subscription,
                        invoice,
                        paymentMethodId
                    }
                }
            }
        }).catch((error) => {
            console.log(error);
            alert(error.message)
        })
    } else {
        return {subscription, priceId, paymentMethodId}
    }
}

const hanldeRequiresPaymentMethod = ({subscription, paymentMethodId, priceId}) => {
    if (subscription.status === 'active') {
        return {subscription, priceId, paymentMethodId}
    } else if (subscription.latest_invoice.payment_intent.status === "requires_payment_method") {
        localStorage.setItem('latestInvoiceId', subscription.latest_invoice.id);
        localStorage.setItem('latestInvoicePaymentIntentStatus', subscription.latest_invoice.payment_intent.status)
        throw {error: {message: 'your card was declined'}}
    }   else {
        return {subscription, priceId, paymentMethodId}
    }
}



const createSubscription = async ({customerId, priceId, paymentMethodId}) => {
    // Need CSRF Token to get aroudn Django's click-jacking protections
    var data = new FormData()
    data.append('csrfmiddlewaretoken', document.querySelector('input[name="csrfmiddlewaretoken"]').value)
    data.append('customerId', customerId)
    data.append('priceId', priceId)
    data.append('paymentMethodId', paymentMethodId)
    data.append('trial', document.querySelector('select#trial').value)
    fetch('/create-subscription', {
        method: 'POST',
        body: data,
    }).then(response => response.json())
    .then((result) => {
        if (result.error) {
            throw result.error
        }
        return result
    }).then((subscription) => {
        return {
            paymentMethodId,
            priceId,
            subscription
        }
    }).then(handlePaymentRequiringCustomerAction)
    .then(hanldeRequiresPaymentMethod)
    .then(onSubscriptionComplete)
    .catch(error => {
        errorMessageHandler(error)}
    )
}

const retryInvoiceWithNewPaymentMethod = ({customerId, paymentMethodId, invoiceId, priceId}) => {
    var data = new FormData()
    data.append('csrfmiddlewaretoken', document.querySelector('input[name="csrfmiddlewaretoken"]').value)
    data.append('customerId', customerId)
    data.append('paymentMethodId', paymentMethodId)
    data.append('invoiceId', invoiceId)
    return (
        fetch('/retry-invoice', {
            method: "POST",
            body: data,
        }).then(resposen => response.json())
        .then((result) => {
            if(result.error) {
                throw result;
            }
            return result;
        }).then((result) => {
            return {
                invoice: result,
                paymentMethodId,
                priceId,
                isRetry: true
            }
        }).then(handlePaymentRequiringCustomerAction)
        .then(onSubcsriptionComplete)
        .catch((error) => {
            console.log(error);
            alert(error.message)
        })
    )
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
            createSubscription({
                customerId,
                priceId,
                paymentMethodId: result.paymentMethod.id,
            })
        }
    })
}

const cancelSubscription = () => {
    const data = new FormData(document.getElementById('cancel-form'));
    return fetch('/cancel-subscription', {
        method: "POST",
        data
    }).then(response => response.json())
    .then(() => {
        M.toast('Your subscription has been canceled')
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




