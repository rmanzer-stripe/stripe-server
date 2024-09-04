"""
    payments/tasks.py
    
    Handle async/mutliprocessing tasks in background.
"""
from logging import Logger
import random
import string
from xmlrpc.client import boolean
import stripe

from django.conf import settings

from celery import shared_task
from celery.utils.log import get_task_logger

from payments import models

logger = get_task_logger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

MODEL_DICT = {
    'account': {'local': models.Account, 'stripe': stripe.Account},
    'invoice': {'local': models.Invoice, 'stripe': stripe.Invoice},
    'charge': {'local': models.Charge, 'stripe': stripe.Charge},
    'customer': {'local': models.Customer, 'stripe': stripe.Customer},
    'payment_intent': {'local': models.PaymentIntent, 'stripe': stripe.PaymentIntent, 'has_fields': True},
    'issuing_dispute': {'local': models.Dispute, 'stripe': stripe.Dispute},
    'product': {'local': models.Product, 'stripe': stripe.Product},
    'price': {'local': models.Price, 'stripe': stripe.Price},
    'subscription': {'local': models.Subscription, 'stripe': stripe.Subscription},
    'coupon': {'local': models.Coupon, 'stripe': stripe.Coupon},
    'promotion_code': {'local': models.PromotionCode, 'stripe': stripe.PromotionCode},
    'terminal.reader': {'local': models.Reader, 'stripe': stripe.terminal.Reader},
    'tax_rate': {'local': models.TaxRate, 'stripe': stripe.TaxRate},
    'setup_intent': {'local': models.SetupIntent, 'stripe': stripe.SetupIntent},

}


@shared_task
def sync_local(model, stripe_object):
    """
    Sync local Stripe object records

    Args:
        model (str): Name of model to be updated
        stripe_object (dict): Stripe object as dictionary
    """

    if model in MODEL_DICT.keys():
        if stripe_object.get('id', False):
            logger.info(f'Updating {model} with ID: {stripe_object["id"]}')
            obj, created = MODEL_DICT[model]['local'].objects.update_or_create(
                id=stripe_object['id'],
                defaults={'data': stripe_object}
            )
            if MODEL_DICT[model].get('has_fields', False):
                obj.update_from_data()
        else:
            logger.warning(
                f'Stripe object did not contain ID attribute: {stripe_object}')


@shared_task
def handle_invoice(stripe_object):
    """
    Setup default payment method for invoices

    Args:
        stripe_object (dict): Stripe invoice object
    """
    if stripe_object.get('billing_reason') == 'subscription_created':
        subscription_id = stripe_object.get('subscription', False)
        payment_intent_id = stripe_object.get('payment_intent', False)

        if all([subscription_id, payment_intent_id]):
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            stripe.Subscription.modify(
                subscription_id,
                default_payment_method=payment_intent['payment_method']
            )
        else:
            raise AttributeError(
                'Invoice did not include subscription or payment_intent details')


@shared_task
def add_app_account(event) -> None:
    """
    Add record of an account that installed my Stripe App

    Args:
        event (dict): Stripe Event object https://stripe.com/docs/api/events/object

    Returns: None
    """
    try:
        acct = stripe.Account.retrieve(event['account'])
        models.AppAccount.create(id=acct.id, data=acct)
    except Exception as e:
        raise e


@shared_task
def rm_app_account(event) -> None:
    """
    Remove App Account record when an account uninstalls the app

    Args:
        event (dict): Stripe event object

    Raises:
        e: Exception due to something not working when we attempt to delete the record
    """
    try:
        models.AppAccount.delete(id=event['account'])
    except Exception as e:
        raise e


def update_invoice_descriptor(object):
    logger.info('Updating Invoice statement descriptor')
    N = 6
    result = ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=N))

    descriptor = f'TEST {result}'

    invoice_id = object.get('id', False)
    if invoice_id:
        stripe.Invoice.modify(invoice_id, statement_descriptor=descriptor)


@shared_task
def process_webhook(event):
    """
    Handle Stripe webhook by updating local object record

    Args:
        event (dict): Stripe webhook event object
    """
    logger.info(f"Event received: {event['type']}")
    event_type = event.get('type', False)
    stripe_object = event.get('data', {}).get('object', {})
    model_name = stripe_object.get('object', False)
    if model_name:
        sync_local.delay(model_name, stripe_object)
    if event_type == "invoice.created":
        update_invoice_descriptor(stripe_object)
    if event_type == "invoice.payment_succeeded":
        handle_invoice.delay(stripe_object)
    if event_type == "issuing_authorization.request" and stripe_object:
        handle_issuing_auth.delay(stripe_object)
    if event_type == "account.application.authorized":
        add_app_account.delay(event)
        logger.info(f'App installed: {event}')
    if event_type == "account.application.deauthorized":
        rm_app_account.delay(event)
        logger.info(f'App uninstalled: {event}')


# -----------------------------------------------------------
#               ISSUING AUTHORIZATIONS
# -----------------------------------------------------------

def check_approval(auth_request: dict) -> boolean:
    """
    Evaluate rules to determine whether charge is authorized

    Args:
        auth_request (dict): The authorization request object

    Returns:
        boolean: Approval decision (True=Yes, False=No)
    """
    transaction = auth_request['pending_request']
    merchant = auth_request['merchant_data']
    currency = auth_request['currency']

    approved = False
    if transaction['amount'] < 5000:
        logger.info('Charge approved by amount threshold')
        approved = True
    if merchant['category'] == 'amusement_parks_carnivals':
        logger.info('Charge approved by category')
        approved = True
    if currency.lower() == "gbp":
        logger.warning('Charge rejected by currency')
        approved = False

    return approved


@shared_task
def handle_issuing_auth(stripe_object):
    approval_outcome = check_approval(stripe_object)
    if approval_outcome:
        logger.info("Charge is approved")
        auth = stripe.issuing.Authorization.approve(stripe_object['id'])
        logger.info(f'Authorization: {auth}')
    else:
        logger.info("charge is rejected")
        stripe.issuing.Authorization.decline(stripe_object['id'])
        logger.info(f'Authorization: {auth}')


@shared_task
def update_local_records():
    """
    Ensure that local records are synced with Stripe objects
    """
    for k, models in MODEL_DICT.items():
        logger.info(f'Updating {k}')
        objs = models['stripe'].list(limit=3)
        for obj in objs.auto_paging_iter():
            models['local'].objects.update_or_create(
                id=obj['id'],
                defaults={'data': obj},
            )
