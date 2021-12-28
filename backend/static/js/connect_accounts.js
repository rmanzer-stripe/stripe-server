/**
 * Custom javascript for connect account integration
 */

stripeInit().then(() => {
    const form = document.getElementById('account-details')
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        const data = new FormData(event.target);
        fetch(form.action, {
            method: "POST",
            body: data
        }).then(response => response.json())
        .then(result => {
            location.href = result.url
        })
    })
})