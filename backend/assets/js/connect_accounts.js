/**
 * Custom javascript for connect account integration
 */

stripeInit().then(() => {
  const form = document.getElementById("account-details");
  if (form) {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const data = new FormData(event.target);
      fetch(form.action, {
        method: "POST",
        body: data,
      })
        .then((response) => response.json())
        .then((result) => {
          location.assign(result.url);
        });
    });
  }
  const checkoutId = new URLSearchParams(window.location.search).get(
    "session_id"
  );
  if (checkoutId) {
    document.querySelector("input#session_id").value = checkoutId;
  }
});
