import stripe

from django.conf import settings
from logging import getLogger

logger = getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


def attach_payment():
    """
    Create and attach payment method to customer
    """

    stripe.api_key = settings.STRIPE_SECRET_KEY
    CUSTOMER_ID = 'cus_KgfkGWhkAYC3ND'
    try:
        payment_method = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": "4242424242424242",
                "exp_month": 12,
                "exp_year": 2022,
                "cvc": "314",
            },
        )
        logger.info(payment_method)
        stripe.PaymentMethod.attach(
            payment_method['id'],
            customer=CUSTOMER_ID
        )
    except Exception as e:
        logger.error(str(e))


def rm_subscriptions():
    """
    Remove incomplete subscriptions
    """

    [
        stripe.Subscription.cancel(s['id'])
        for s in stripe.Subscription.list(
            status='incomplete', limit=100)['data']
    ]


def rm_empty_customers():
    """
    Remove customers without a name
    """
    customers = stripe.Customer.list(limit=10)
    for customer in customers.auto_paging_iter():
        if customer['name'] == None or customer['name'] == 'Old Subscription Flow':
            stripe.Customer.delete(customer['id'])


def list_of_stuff(list: list, redact: bool):
    """_summary_

    Args:
        list (list): _description_
        redact (bool): _description_
    """
