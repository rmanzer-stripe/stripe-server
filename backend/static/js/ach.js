// Create Token and process response
// https://stripe.com/docs/js/tokens_sources/create_token?type=bank_account

const bankInfoProto = {
    country: 'US',
    currency: 'usd',
    account_holder_type: 'individual',
}

const getValById = (id) => {
    return document/getValById(id).value
}

const achHandler = (event) => {
    const errDiv = document.getElementById('card-errors');
    if (event.error) {
        errDiv.textContent = event.error.message;
        errDiv.style.display = 'block';
    } else if (event.token) {
        document.getElementById('tokenId').setAttribute('value',event.token.id);
        document.getElementById('bank-info').submit();
    } else {
        errDiv.textContent = ''
        errDiv.style.display = 'none'
    }
}

// Calling initialization of stripe and then loading event handlers
stripeInit().then(() => {
    document.getElementById('bank-info').addEventListener('submit', (e) => {
        e.preventDefault();
        const bankInfo = {
            ...bankInfoProto,
            account_holder_name: document.getElementById('accountName').value,
            account_number: document.getElementById('accountNumber').value,
            routing_number: document.getElementById('routingNumber').value
        }
        stripe.createToken('bank_account', bankInfo).then(achHandler);
    })
    
})

const achTest = () => {
    stripe
  .createToken('bank_account', {
    country: 'US',
    currency: 'usd',
    routing_number: '110000000',
    account_number: '000123456789',
    account_holder_name: 'Jenny Rosen',
    account_holder_type: 'individual',
    // account_type: 'checking',
  })
  .then(function(result) {
    console.log(result)
  });

}
