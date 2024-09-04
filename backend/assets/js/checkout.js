// Defining PaymentIntent UPE checkout methods

const form = document.getElementById("payment-form");

const appearance = {
  // theme: "stripe",
  // variables: {
  //   fontWeightNormal: "500",
  //   borderRadius: "2px",
  //   colorPrimary: "#f360a6",
  //   colorIconTabSelected: "#fff",
  //   spacingGridRow: "16px",
  // },
  // rules: {
  //   ".Tab, .Input, .Block, .CheckboxInput, .CodeInput": {
  //     boxShadow: "0px 3px 10px rgba(18, 42, 66, 0.08)",
  //   },
  //   ".Block": {
  //     borderColor: "transparent",
  //   },
  //   ".BlockDivider": {
  //     backgroundColor: "#ebebeb",
  //   },
  //   ".Tab, .Tab:hover, .Tab:focus": {
  //     border: "0",
  //   },
  //   ".Tab--selected, .Tab--selected:hover": {
  //     backgroundColor: "#f360a6",
  //     color: "#fff",
  //   },
  // },
};

const options = {
  clientSecret: form.dataset.secret,
  appearance: appearance,
  fonts: [
    {
      cssSrc: "https://fonts.googleapis.com/css2?family=Montserrat",
    },
  ],
};

fetch("/config/")
  .then((response) => response.json())
  .then((data) => {
    var stripe = Stripe(data.publicKey, {
      apiVersion: "2020-08-27",
      stripeAccount: "acct_1L6fbfRMSufZOWVI",
      // locale: "fr",
    });
    if (document.getElementById("api_key")) {
      stripe = Stripe(document.getElementById("api_key").dataset.key);
    }

    const elements = stripe.elements(options);
    const payOptions = {
      paymentMethodOrder: [
        "apple_pay",
        "klarna",
        "afterpay_clearpay",
        "google_pay",
        "alipay",
      ],
      terms: {
        card: "always",
        usBankAccount: "always",
      },
      fields: {
        billing_details: {
          name: "auto",
        },
      },
    };

    // const addressElement = elements.create("address", {
    //   mode: "shipping",
    //   // display: { name: "split" },
    // });
    // addressElement.mount("#address-element");

    // addressElement.on("change", (e) => {
    //   console.log(e);
    // });

    const paymentElement = elements.create("payment", payOptions);
    paymentElement.mount("#payment-element");

    paymentElement.on("change", (e) => {
      console.log(e);
    });
    paymentElement.on("network", (e) => {
      console.log(e);
    });

    form.addEventListener("submit", async (event) => {
      event.preventDefault();

      const { error } = await stripe.confirmPayment({
        elements,
        confirmParams: {
          return_url: `${window.location.origin}/success`,
        },
      });

      if (error) {
        console.log(error);
        const messsageContainer = document.querySelector("#error-message");
        messsageContainer.textContent = error.message;
        messsageContainer.style.display = "block";
      } else {
        // console.log(resp);
        M.toast({ html: "Success" });
      }
    });
  });
