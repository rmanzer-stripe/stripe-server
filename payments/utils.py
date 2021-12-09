import stripe

from django.conf import settings
from logging import getLogger

logger = getLogger(__name__)


def attach_payment() -> None:
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
