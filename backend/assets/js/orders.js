// Defining PaymentIntent UPE checkout methods

const form = document.getElementById("payment-form");

const options = {
  clientSecret: form.dataset.secret,
  appearance: { theme: "night", labels: "floating" },
};

fetch("/config/")
  .then((response) => response.json())
  .then((data) => {
    var stripe = Stripe(data.publicKey, {
      betas: ["process_order_beta_1"],
      apiVersion: "2020-08-27; orders_beta=v2",
    });
    const elements = stripe.elements(options);
    const payOptions = { fields: { billingDetails: { address: "auto" } } };
    const paymentElement = elements.create("payment", payOptions);
    paymentElement.mount("#payment-element");

    form.addEventListener("submit", async (event) => {
      event.preventDefault();

      const resp = await stripe.processOrder({
        //`Elements` instance that was used to create the Payment Element
        elements,
        confirmParams: {
          return_url: "https://rmanzer-app.tunnel.stripe.me/success",
        },
      });
      console.log(resp);
      if (error) {
        // This point will only be reached if there is an immediate error when
        // confirming the payment. Show error to your customer (for example, payment
        // details incomplete)
        const messageContainer = document.querySelector("#error-message");
        messageContainer.textContent = error.message;
      } else {
        // Your customer will be redirected to your `return_url`. For some payment
        // methods like iDEAL, your customer will be redirected to an intermediate
        // site first to authorize the payment, then redirected to the `return_url`.
      }

      //   subForm = new FormData(document.getElementById("orderSubmit"));
      //   const resp = await fetch("/orders/", {
      //     method: "POST",
      //     body: subForm,
      //   });
      //   console.log(resp);

      //   const { error } = await stripe.confirmPayment({
      //     //`Elements` instance that was used to create the Payment Element
      //     elements,
      //     confirmParams: {
      //       return_url: "https://rmanzer-app.tunnel.stripe.me/success",
      //     },
      //   });

      //   if (error) {
      //     // This point will only be reached if there is an immediate error when
      //     // confirming the payment. Show error to your customer (for example, payment
      //     // details incomplete)
      //     const messageContainer = document.querySelector("#error-message");
      //     messageContainer.textContent = error.message;
      //   } else {
      //     // Your customer will be redirected to your `return_url`. For some payment
      //     // methods like iDEAL, your customer will be redirected to an intermediate
      //     // site first to authorize the payment, then redirected to the `return_url`.
      //   }
    });
  });
