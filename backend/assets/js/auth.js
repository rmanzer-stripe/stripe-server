var auth_stripe,
  stripe_elements,
  stripe_card_number,
  stripe_ideal_bank,
  stripe_payment_request;
const STRIPE_IDEAL_ID = "stripe-ideal--element";
const STRIPE_PAYREQ_ID = "stripe-payment-request--element";
$(function () {
  "use strict";
  if (typeof Stripe === "undefined" || typeof STRIPE_PK === "undefined")
    alert(__("checkout_error_payment"));
  else {
    initStripe();
    initStripeCardForm();
    if (dgid(STRIPE_IDEAL_ID) !== null) initStripeIdealForm();
    if (dgid(STRIPE_PAYREQ_ID) !== null) initStripePaymentRequestButton();
  }
});
function initStripe() {
  auth_stripe = Stripe(STRIPE_PK, CODE_LANG);
  stripe_elements = auth_stripe.elements();
}
function initStripeCardForm() {
  var custom_input_style = {
    letterSpacing: "2px",
    fontSize:
      16 + ((19 - 16) * (window.innerWidth - 1024)) / (2100 - 1024) + "px",
    fontFamily: "Monaco, monospace",
    color: "#2e2e2e",
    lineHeight: 1.5,
    "::placeholder": { color: "rgba(156, 156, 156, 0.5)" },
    ":focus::placeholder": { color: "rgba(156, 156, 156, 0.15)" },
  };
  stripe_card_number = stripe_elements.create("cardNumber", {
    placeholder: "8888 8888 8888 8888",
    showIcon: false,
  });
  stripe_card_number.mount("#stripe-encrypted-form-number");
  var stripe_card_expiry = stripe_elements.create("cardExpiry", {});
  stripe_card_expiry.mount("#stripe-encrypted-form-expiry");
  var stripe_card_cvc = stripe_elements.create("cardCvc", {
    placeholder: "888",
  });
  stripe_card_cvc.mount("#stripe-encrypted-form-cvc");
  [stripe_card_number, stripe_card_expiry, stripe_card_cvc].forEach(function (
    element
  ) {
    element.addEventListener("change", function (event) {
      var errorDiv = dgid("credit-card-stripe-error"),
        errorText = dgid("credit-card-stripe-error--" + event.elementType),
        errorTextList = errorDiv.getElementsByClassName("label-info");
      errorText.textContent = event.error ? event.error.message : "";
      var hasErrors = false;
      for (var i = 0; i < errorTextList.length; ++i) {
        var p = errorTextList[i];
        if ((hasErrors = p.textContent != "")) break;
      }
      errorDiv.style.display = hasErrors ? "block" : "none";
    });
  });
  var form = dgid("process-purchase");
  form.elements["card-name"].addEventListener("change", function (event) {
    var errorDiv = dgid("credit-card-stripe-error"),
      errorText = dgid("credit-card-stripe-error--cardName");
    errorText.textContent = this.value == "" ? __("card_error_name") : "";
    errorDiv.style.display = this.value == "" ? "block" : "none";
  });
}
function initStripeIdealForm() {
  var custom_input_style = {
    letterSpacing: "2px",
    fontSize:
      16 + ((19 - 16) * (window.innerWidth - 1024)) / (2100 - 1024) + "px",
    fontFamily: "Monaco, monospace",
    color: "#2e2e2e",
    lineHeight: 1.5,
    "::placeholder": { color: "rgba(156, 156, 156, 0.5)" },
    ":focus::placeholder": { color: "rgba(156, 156, 156, 0.15)" },
    padding: "10px 12px",
  };
  stripe_ideal_bank = stripe_elements.create("idealBank", {});
  stripe_ideal_bank.mount("#" + STRIPE_IDEAL_ID);
}
function initStripePaymentRequestButton() {
  const valid_countries = [
    "AE",
    "AT",
    "AU",
    "BE",
    "BG",
    "BR",
    "CA",
    "CH",
    "CI",
    "CR",
    "CY",
    "CZ",
    "DE",
    "DK",
    "DO",
    "EE",
    "ES",
    "FI",
    "FR",
    "GB",
    "GR",
    "GT",
    "HK",
    "HU",
    "ID",
    "IE",
    "IN",
    "IT",
    "JP",
    "LT",
    "LU",
    "LV",
    "MT",
    "MX",
    "MY",
    "NL",
    "NO",
    "NZ",
    "PE",
    "PH",
    "PL",
    "PT",
    "RO",
    "SE",
    "SG",
    "SI",
    "SK",
    "SN",
    "TH",
    "TT",
    "US",
    "UY",
  ];
  if (valid_countries.indexOf(CODE_COUNTRY) == -1) return false;
  stripe_payment_request = auth_stripe.paymentRequest({
    country: CODE_COUNTRY,
    currency: CURRENCY_ISO.toLowerCase(),
    total: {
      label: ___("miscota_purchase", { SHOP_NAME: SHOP_NAME }),
      amount: fixCurrencySubunit(dgid("total_price").value, CURRENCY_ISO),
    },
  });
  stripe_payment_request.canMakePayment().then(function (result) {
    if (result && !result.applePay) {
      var paymethodContainer = dgid(STRIPE_PAYREQ_ID).parentElement;
      var paymethodName = dgid("stripe-payment-request--name");
      if (result.applePay) {
        paymethodContainer.classList.add("apple-pay");
        paymethodName.innerText = "Apple Pay";
      } else if (window.navigator.userAgent.indexOf("Edge") != -1) {
        paymethodContainer.classList.add("microsoft-pay");
        paymethodName.innerText = "Microsoft Pay";
      } else {
        paymethodContainer.classList.add("google-pay");
        paymethodName.innerText = "Google Pay";
      }
      paymethodContainer.classList.remove("hide");
    }
  });
}
function doPaymentStripe(clientSecret, finishFunc) {
  if (typeof finishFunc != "function")
    finishFunc = function () {
      gotoPayment(false);
    };
  var form = dgid("process-purchase");
  var brandCode = $('input[name="payment-method"]:checked').attr("method");
  switch (brandCode) {
    case "ideal":
      return doPaymentStripeIdeal(clientSecret);
    case "bancontact":
      return doPaymentStripeBancontact(clientSecret);
    case "giropay":
      return doPaymentStripeGiropay(clientSecret);
    case "p24":
      return doPaymentStripePrzelewy24(clientSecret);
    case "eps":
      return doPaymentStripeEPS(clientSecret);
    case "payment-request":
      return doPaymentRequest(clientSecret);
    case "sofort":
      return doPaymentStripeSofort(clientSecret);
    default:
      if (brandCode) return doPaymentStripeSources(brandCode);
  }
  if (!USER_LOGGED) {
    var postcode = form.elements["postcode"].value;
  } else {
    var idAddress = form.checkedVal("shipping_address");
    var postcode = $("#shipping-address" + idAddress)
      .find(".postalcode")
      .text()
      .replace(/(\r\n|\n|\r)/gm, " ")
      .trim();
  }
  var selected_card = form.selected_card.value;
  if (selected_card) {
    var confirm_opts = { payment_method: selected_card };
  } else {
    if (form.elements["card-name"].value == "") {
      var errorDiv = dgid("credit-card-stripe-error"),
        errorText = dgid("credit-card-stripe-error--cardName");
      errorText.textContent = __("card_error_name");
      errorDiv.style.display = "block";
      cancelStripeFormSend();
      return false;
    }
    var confirm_opts = {
      payment_method: {
        card: stripe_card_number,
        billing_details: {
          name: form.elements["card-name"].value,
          address: { postal_code: postcode },
        },
      },
    };
    if (form.elements["recurring"].checked) {
      confirm_opts["setup_future_usage"] = "off_session";
    }
  }
  auth_stripe
    .confirmCardPayment(clientSecret, confirm_opts)
    .then(function (result) {
      __confirmPaymentResult(result, form, finishFunc);
    });
}
function __confirmPaymentResult(result, form, finishFunc) {
  if (result.error) {
    $.post("/cart/logStripeErrors", { error: result.error });
    var errorDiv = ContentErrorCheckout(result.error.message, true);
    cancelStripeFormSend();
  } else if (
    form &&
    finishFunc &&
    (result.paymentIntent.status === "succeeded" ||
      result.paymentIntent.status === "capture_payment")
  ) {
    if (form.autoship && form.autoship.value == "1") {
      var data =
        $(form).serialize() +
        "&stripe_payment_method=" +
        result.paymentIntent.payment_method +
        "&is_stripe=true";
      $.post("/order_form/createAutoshippingCart", data, finishFunc);
    } else {
      finishFunc();
    }
  } else {
    finishFunc();
  }
}
function doPaymentStripeIdeal(clientSecret) {
  auth_stripe
    .confirmIdealPayment(clientSecret, {
      payment_method: { ideal: stripe_ideal_bank },
      return_url: window.location.origin + "/checkout/payment/stripe",
    })
    .then(function (result) {
      __confirmPaymentResult(result);
    });
}
function doPaymentStripeBancontact(clientSecret) {
  auth_stripe
    .confirmBancontactPayment(clientSecret, {
      payment_method: { billing_details: { name: getBillingDetailsName() } },
      return_url: window.location.origin + "/checkout/payment/stripe",
    })
    .then(function (result) {
      __confirmPaymentResult(result);
    });
}
function doPaymentStripeGiropay(clientSecret) {
  auth_stripe
    .confirmGiropayPayment(clientSecret, {
      payment_method: { billing_details: { name: getBillingDetailsName() } },
      return_url: window.location.origin + "/checkout/payment/stripe",
    })
    .then(function (result) {
      __confirmPaymentResult(result);
    });
}
function doPaymentStripePrzelewy24(clientSecret) {
  auth_stripe
    .confirmP24Payment(clientSecret, {
      payment_method: { billing_details: { email: getBillingDetailsEmail() } },
      return_url: window.location.origin + "/checkout/payment/stripe",
    })
    .then(function (result) {
      __confirmPaymentResult(result);
    });
}
function doPaymentStripeSofort(clientSecret) {
  auth_stripe
    .confirmSofortPayment(clientSecret, {
      payment_method: {
        sofort: { country: CODE_COUNTRY },
        billing_details: {
          email: getBillingDetailsEmail(),
          name: getBillingDetailsName(),
        },
      },
      return_url: window.location.origin + "/checkout/payment/stripe",
    })
    .then(function (result) {
      __confirmPaymentResult(result);
    });
}
function doPaymentStripeEPS(clientSecret) {
  auth_stripe
    .confirmEpsPayment(clientSecret, {
      payment_method: { billing_details: { name: getBillingDetailsName() } },
      return_url: window.location.origin + "/checkout/payment/stripe",
    })
    .then(function (result) {
      __confirmPaymentResult(result);
    });
}
function doPaymentRequest(clientSecret) {
  stripe_payment_request.on("paymentmethod", function (ev) {
    var form = dgid("process-purchase");
    var confirm_opts = {};
    if (form.elements["recurring-payreq"].checked)
      confirm_opts["setup_future_usage"] = "off_session";
    confirm_opts["payment_method"] = ev.paymentMethod.id;
    auth_stripe
      .confirmCardPayment(clientSecret, confirm_opts)
      .then(function (result) {
        if (result.error) {
          ev.complete("fail");
          $.post("/cart/logStripeErrors", { error: result.error });
          var errorDiv = ContentErrorCheckout(result.error.message);
          cancelStripeFormSend();
        } else {
          ev.complete("success");
          __confirmPaymentResult(result, form, function () {
            gotoPayment(false);
          });
        }
      });
  });
  stripe_payment_request.on("cancel", cancelStripeFormSend);
  stripe_payment_request.show();
}
function doPaymentStripeSources(brandCode) {
  var form = dgid("process-purchase");
  var klarnaType = form["klarna-method"] ? form["klarna-method"].value : "";
  if (brandCode == "klarna" && !klarnaType) {
    cancelStripeFormSend();
    alert(__("klarna_choose_paymethod"));
    return;
  }
  $.get(
    "/cart/createSource/" + brandCode,
    function (source) {
      if (source.type == "klarna") {
        var form = dgid("process-purchase");
        var klarnaType = form["klarna-method"].value;
        var redirectKey = klarnaType + "_redirect_url";
        if (redirectKey in source.klarna) {
          window.location.replace(source.klarna[redirectKey]);
        } else {
          $('.klarna .input--payment-info [id$="--container"]').hide();
          var categories = source.klarna.payment_method_categories.split(",");
          for (var i = 0; i < categories.length; ++i)
            $("#klarna_" + categories[i] + "--container").show();
          cancelStripeFormSend();
          alert(__("klarna_choose_paymethod"));
        }
      } else if (source.flow == "redirect") {
        window.location.replace(source.redirect.url);
      } else if (source.flow == "receiver") {
        window.location.replace(
          source.redirect.return_url + "?source=" + source.id
        );
      }
    },
    "json"
  );
}
function cancelStripeFormSend() {
  $(".loading-wrapper").closest(".popUpContainer").remove();
  setTimeout(function () {
    $(".purchase-button").attr("disabled", false);
  }, 1000);
}
function fixCurrencySubunit(total, currency_iso) {
  return currency_iso in
    [
      "BIF",
      "CLP",
      "DJF",
      "GNF",
      "JPY",
      "KMF",
      "KRW",
      "MGA",
      "PYG",
      "RWF",
      "UGX",
      "VND",
      "VUV",
      "XAF",
      "XOF",
      "XPF",
    ]
    ? total
    : parseFloat((total * 100).toFixed(0));
}
function getBillingDetailsName() {
  var form = dgid("process-purchase");
  if (form.custom_address.value == "1") {
    return (form.name.value + " " + form.lastname.value).trim();
  } else {
    var idAddress = form.checkedVal("shipping_address");
    return $("#shipping-address" + idAddress)
      .find(".complete-name")
      .text()
      .replace(/(\r\n|\n|\r)/gm, " ")
      .trim();
  }
}
function getBillingDetailsEmail() {
  var form = dgid("process-purchase");
  return form.email.value;
}
