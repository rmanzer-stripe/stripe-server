/**
 * Display error if exists, otherwise clear error div
 * @param {Object} error error object returned by Stripe API
 */
const errMessageHandler = (error) => {
  const errDiv = document.getElementById("error-message");
  if (error) {
    errDiv.textContent = error.message;
    errDiv.style.display = "block";
  } else {
    errDiv.textContent = "";
    errDiv.style.display = "none";
  }
};

stripeInit({ locale: "it" }).then(() => {
  const options = {
    clientSecret: document.getElementById("client-secret").value,
    appearance: {
      theme: "night",
      labels: "floating",
    },
  };

  const elements = stripe.elements(options);

  const paymentElement = elements.create("payment");
  paymentElement.mount("#payment-element");
  // paymentElement.on('change', event => {console.log(event)})
  const form = document.getElementById("setup-form");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    console.log(elements);
    const { setupIntent, error } = await stripe.confirmSetup({
      elements,
      confirmParams: {
        return_url: "https://example.com",
      },
    });
    if (error) {
      console.error(error.message);
    } else {
      console.log(setupIntent);
    }
  });
});

// USER FUNCTIONS - I NEED SYNTAX HIGHLIGHTS
// private initCardSection(): void {     this.paymentService.getSetupIntent().subscribe((setupIntent: SetupIntent) => {       this.setupIntent = setupIntent;       loadStripeScript(() => {         // ToDo move Key to config         this.stripe = Stripe(environment.stripe.api_key);         const elements = this.stripe.elements();         this.stripeCard = elements.create('card');         this.stripeCard.mount(this.cardElement.nativeElement);         this.stripeCard.addEventListener('change', ({error}) => {           this.cardErrorMessage = error && error.message;         });       });     });   }
