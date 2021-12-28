// Separate JS file to set up Request Button
// https://stripe.com/docs/stripe-js/elements/payment-request-button?platform=html-js-testing-chrome#html-js-testing




stripeInit().then(() => {
    const paymentRequest = stripe.paymentRequest({
        country: 'US',
        currency: 'usd',
        total: {
            label: 'demo total',
            amount: 100
        },
        requestPayerName: true,
        requestPayerEmail: true,
    });
    const clientSecret = document.getElementById('clientSecret').value
    // console.log(clientSecret);
    const elements = stripe.elements();
    const prButton = elements.create('paymentRequestButton', { paymentRequest });

    paymentRequest.canMakePayment().then((result) => {
        if (result) {
            prButton.mount('#payment-request-button');
        } else {
            document.getElementById('payment-request-button').style.display = 'none';
        }
    });

    paymentRequest.on('paymentmethod', (ev) => {
        stripe.confirmCardPayment(
            clientSecret,
            {payment_method: ev.paymentMethod.id},
            {handleActions: false}
        ).then((confirmResult)=> {
            if(confirmResult.error) {
                ev.complete('fail')
            } else {
                ev.complete('success');

                if(confirmResult.paymentIntent.status === 'requires_action') {
                    stripe.confirmCardPayment(clientSecret).then((result) => {
                        if (result.error) {
                            messageModal("Please provide a new payment method", "Payment Failed")
                        } else {
                            messageModal("You have successfully paid for stuff.  Thank you!", "Payment Succeeded")
                        }
                    })
                } else {
                    messageModal("This was successful, whatever that means", 'Success')
                }
            }
        })
    });
})