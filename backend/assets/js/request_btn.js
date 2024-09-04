// Separate JS file to set up Request Button
// https://stripe.com/docs/stripe-js/elements/payment-request-button?platform=html-js-testing-chrome#html-js-testing

stripeInit().then(() => {
  const paymentRequest = stripe.paymentRequest({
    country: "US",
    currency: "usd",
    total: {
      label: "Amount not charged",
      amount: 0,
      pending: true,
    },
    disableWallets: ["link"],
    requestPayerName: true,
    requestPayerEmail: true,
    requestPayerPhone: true,
    requestShipping: true,
    shippingOptions: [
      {
        id: "ground",
        label: "Ground Shipping",
        detail: "3 day ground shipping via UPS",
        amount: 1095,
      },
      {
        id: "air",
        label: "Air Shipping",
        detail: "Next day ground shipping via DHL",
        amount: 2595,
      },
    ],
  });
  const clientSecret = document.getElementById("clientSecret").value;
  const isSetup = clientSecret.startsWith("seti_");
  console.log(clientSecret);
  const elements = stripe.elements();
  const prButton = elements.create("paymentRequestButton", { paymentRequest });

  paymentRequest.canMakePayment().then((result) => {
    console.log(result);
    if (result) {
      prButton.mount("#payment-request-button");
    } else {
      document.getElementById("payment-request-button").style.display = "none";
    }
  });
  paymentRequest.on("change", (ev) => {
    console.log(ev);
  });

  paymentRequest.on("click", (ev) => {
    console.log("PRB clicked");
  });

  paymentRequest.on("paymentmethod", (ev) => {
    console.log("Payment Method", ev);
  });

  paymentRequest.on("shippingaddresschange", (e) => {
    console.log(e.shippingAddress);
    const status = ["US", "BR", "HK"].includes(e.shippingAddress.country)
      ? "success"
      : "invalid_shipping_address";
    const updateDetails = { status: status };
    console.log(updateDetails);
    e.updateWith(updateDetails);
  });

  paymentRequest.on("paymentmethod", (ev) => {
    let confirmFunc = null;
    if (isSetup) {
      confirmFunc = stripe.confirmCardSetup;
    } else {
      confirmFunc = stripe.confirmCardPayment;
    }
    confirmFunc(
      clientSecret,
      { payment_method: ev.paymentMethod.id },
      { handleActions: false }
    ).then((confirmResult) => {
      console.log(confirmResult);
      if (confirmResult.error) {
        ev.complete("fail");
      } else {
        ev.complete("success");

        if (confirmResult.paymentIntent.status === "requires_action") {
          stripe.confirmCardPayment(clientSecret).then((result) => {
            if (result.error) {
              messageModal(
                "Please provide a new payment method",
                "Payment Failed"
              );
            } else {
              messageModal(
                "You have successfully paid for stuff.  Thank you!",
                "Payment Succeeded"
              );
            }
          });
        } else {
          messageModal("This was successful, whatever that means", "Success");
        }
      }
    });
  });
});
