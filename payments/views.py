
import stripe
import pprint
import logging
import json
import uuid
from datetime import datetime, timedelta

from pathlib import Path
from math import ceil

from django.views import generic
from django.conf import settings
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.http.request import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from stripe.api_resources.checkout import session


from payments.forms import EvidenceForm
from payments import models


printer = pprint.PrettyPrinter(indent=4)
pprinter = printer.pprint
logger = logging.getLogger(__name__)


def print_event(msg: str, data: dict, n=100):
    """Print event details to stdout

    Args:
        msg (str): Header message
        data (dict): Event data
        n (int, optional): Number of = printed to start, end. Defaults to 100.

    Returns:
        None: All information printed to screen
    """
    print('='*n)
    print(f'\n{msg}\n')
    printer.pprint(data)
    print('='*n)


def get_host(request: HttpRequest):
    """
    Return host string based on request headers

    Args:
        request (HttpRequest): Request object
    Returns:
        str: Host string
    """
    return f"{request.scheme}://{request.headers['Host']}"


def get_customer(name='Phillip Marlowe'):
    """
    Return Stripe customer object

    Args:
        name (str, optional): Name of a customer. Defaults to 'Phillip Marlowe'.

    Returns:
        [dict]: Customer object as dictionary
    """
    customerRec = models.Customer.objects.filter(
        data__name=name)
    if customerRec:
        customer = stripe.Customer.retrieve(
            customerRec[0].id
        )
        customerRec[0].data = customer
        customerRec[0].save()
    else:
        customer = stripe.Customer.create(
            name=name,
            description="Southern California gumshoe",
        )
        models.Customer.objects.create(
            id=customer['id'],
            data=customer
        )
    return customer

# ---------------------------------------------------------------------------
#                       ClASS BASED VIEWS
# https://docs.djangoproject.com/en/3.2/topics/class-based-views/
# ---------------------------------------------------------------------------


class HomePageView(generic.TemplateView):
    template_name = 'home.html'


class SuccessView(generic.TemplateView):
    template_name = 'success.html'


class CancelledView(generic.TemplateView):
    template_name = 'cancelled.html'


class DisputeList(generic.TemplateView):
    template_name = 'dispute_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        context['disputes'] = stripe.Dispute.list(limit=100)
        return context


class ProvideEvidence(generic.FormView):
    template_name = 'evidence_form.html'
    form_class = EvidenceForm
    success_url = reverse_lazy('payments:dispute-list')

    def get(self, request, *args, **kwargs):
        resp = super().get(request, *args, **kwargs)
        resp.context_data['form'].fields['dispute_id'].initial = kwargs['id']
        return resp

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        form = EvidenceForm(request.POST)
        if form.is_valid():
            disp_id = form.cleaned_data.pop('dispute_id')
            response = stripe.Dispute.modify(
                disp_id,
                evidence=form.cleaned_data
            )
            logger.info(response)
        resp = super().post(request, *args, **kwargs)
        return resp


class PaymentIntent(generic.TemplateView):
    template_name = 'pi_checkout.html'

    def get_customer(self):
        customerRec = models.Customer.objects.filter(
            data__name='Phillip Marlowe')
        if customerRec:
            customer = stripe.Customer.retrieve(
                customerRec[0].id
            )
            customerRec[0].data = customer
            customerRec[0].save()
        else:
            customer = stripe.Customer.create(
                name="Phillip Marlowe",
                description="Southern California gumshoe",
            )
            models.Customer.objects.create(
                id=customer['id'],
                data=customer
            )
        return customer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        logger.info('Getting/Creating customer')
        customer = self.get_customer()
        logger.info('Setting up payment intent')

        idemp_key = str(uuid.uuid4())
        intent = stripe.PaymentIntent.create(
            customer=customer['id'],
            amount=14000,
            currency='usd',
            metadata={'integration_check': 'accept_a_payment',
                      'message': 'stuff is great, I like stuff.'},
            idempotency_key=idemp_key,
            setup_future_usage='off_session',
            automatic_payment_methods={
                'enabled': True
            }
        )
        context['client_secret'] = intent.client_secret
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        printer.pprint(request.headers)
        return response


class PaymentIntentHold(generic.TemplateView):
    template_name = 'pi_checkout2.html'

    def generate_response(self, intent):
        logger.info(intent)
        if intent.status == 'requires_action' and intent.next_action.type == 'use_stripe_sdk':
            # Tell the client to handle the action
            return JsonResponse({
                'requires_action': True,
                'payment_intent_client_secret': intent.client_secret
            })
        elif intent.status == 'succeeded':
            return JsonResponse({'success': True}, status=200)
        elif intent.status == 'requires_capture':
            return JsonResponse({'message': 'Your payment details have been captured and you will be billed later'})
        else:
            return JsonResponse({'error': 'Invalid PaymentIntent status'}, status=500)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        logger.info(data)
        intent = None
        try:
            if 'payment_method_id' in data.keys():
                stripe.api_key = settings.STRIPE_SECRET_KEY
                intent = stripe.PaymentIntent.create(
                    payment_method=data['payment_method_id'],
                    amount=1099,
                    currency='usd',
                    confirm=True,
                    confirmation_method='manual',
                )
            elif 'payment_intent_id' in data:
                intent = stripe.PaymentIntent.confirm(
                    data['payment_intent_id'])
        except stripe.error.CardError as e:
            return JsonResponse({'error': e.user_message}, status=500)

        return self.generate_response(intent)


class CapturePayments(generic.TemplateView):
    template_name = 'capture_payments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        intents = list(filter(lambda pi: pi.status ==
                       'requires_capture', stripe.PaymentIntent.list(limit=100)))
        context['intents'] = intents
        return context

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        pi_id = request.POST['id']
        amount_to_capture = request.POST['amount_to_capture']
        amount_to_capture = None if amount_to_capture == '' else int(
            amount_to_capture)
        capture = bool(request.POST.get('capture', False))
        if not capture:
            stripe.PaymentIntent.cancel(pi_id)
        else:
            stripe.PaymentIntent.capture(
                pi_id,
                amount_to_capture=amount_to_capture
            )
        return HttpResponseRedirect(reverse_lazy('payments:capture'))


class UPE(generic.TemplateView):
    template_name = 'payment_upe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.create(
            amount=14000,
            currency="usd",
            payment_method_types=['card', ],
        )
        context['client_secret'] = intent.client_secret
        return context


class RequestBtn(generic.TemplateView):
    template_name = 'request_btn.html'

    def get_context_data(self, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.ApplePayDomain.create(
            domain_name="https://rmanzer-foo.tunnel.stripe.me"
        )
        intent = stripe.PaymentIntent.create(
            amount=12099,
            currency='usd',
        )
        context = super().get_context_data(**kwargs)
        context['client_secret'] = intent.client_secret
        return context


class PaymentIntentRefund(generic.TemplateView):

    template_name = 'pi_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        intents = list(filter(lambda pi: pi.status != "canceled",
                       stripe.PaymentIntent.list(limit=50)))
        context['intents'] = intents
        return context

    def post(self, request, *args, **kwargs):
        # TODO:  Add form handling for full & partial refunds and cancelling here.
        stripe.api_key = settings.STRIPE_SECRET_KEY
        action = request.POST.get('action', False)
        intent_id = request.POST.get('intent_id', False)
        if intent_id:
            if action == "refund":
                amount = request.POST.get('amount', 0)
                try:
                    response = stripe.Refund.create(
                        amount=amount,
                        payment_intent=intent_id
                    )
                    if response['status'] == 'succeeded':
                        messages.success('Refund processed')
                except stripe.error.InvalidRequestError as e:
                    messages.error(request, f"{e.user_message}")
            if action == "cancel":
                response = stripe.PaymentIntent.cancel(intent_id)

                if response['status'] == "canceled":
                    messages.info(request, "Payment Intent canceled")
            return HttpResponseRedirect(reverse_lazy('payments:payment-refund'))
        else:
            raise AttributeError("No `intent_id` provided")


class LegacyElementPage(generic.TemplateView):
    template_name = 'legacy_element.html'

    def handle_customer(self, customer_name, token):
        customer = models.Customer.objects.filter(data__name=customer_name)
        if customer:
            customer = customer[0]
            customer = stripe.Customer.retrieve(customer.id)
        else:
            customer = stripe.Customer.create(
                name=customer_name,
                source=token
            )
            models.Customer.objects.create(
                id=customer.id,
                data=customer
            )
        return customer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # If necessary, do runtime stuff here
        return context

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        token = request.POST['stripeToken']
        customer_name = request.POST.get('cardholderName', False)
        try:
            if bool(customer_name):
                customer = self.handle_customer(customer_name, token)
            kwargs = {
                'amount': 2000,
                'currency': 'usd',
                'description': 'Legacy Example',
                'source': token,
                'statement_descriptor': 'Nifty stuff'
            }
            if customer:
                kwargs['customer'] = customer.id
                kwargs.pop('source')
            charge = stripe.Charge.create(**kwargs)
            messages.success(request, f'Charge created: {charge.id}')
        except stripe.error.CardError as e:
            msg = f"""
                Request status: {e.http_status}\n
                Code: {e.code}\n
                Param: {e.param}\n
                Message: {e.user_message}
            """
            messages.error(request, msg)
        except Exception as e:
            messages.error(request, str(e))
        return HttpResponseRedirect(reverse_lazy('payments:legacy-payment'))


class ACHCharge(generic.TemplateView):
    template_name = 'ach_charge.html'

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        token = request.POST['stripeToken']
        customer_name = request.POST.get('cardholderName', False)
        try:
            customer = stripe.Customer.create(
                name=customer_name,
                source=token
            )
            bank_account = stripe.Customer.retrieve_source(
                customer.id,
                customer.default_source
            )
            bank_account.verify(amounts=[32, 45])
            stripe.Charge.create(
                amount=5000, currency="usd", customer=customer.id)
            messages.success(
                request, 'Account logged and verified and $50 charged')
            return HttpResponseRedirect(reverse_lazy('payments:ach'))
        except Exception as e:
            messages.error(request, str(e))


class SetupIntent(generic.TemplateView):
    template_name = 'setup_intent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        customer = get_customer()
        idemp_key = str(uuid.uuid4())
        intent = stripe.SetupIntent.create(
            customer=customer['id'],
            payment_method_types=['card', 'ideal', 'bancontact'],
            idempotency_key=idemp_key
        )
        context['setup_intent'] = intent.client_secret
        context['customer_id'] = customer['id']
        context['return_url'] = reverse_lazy('payments:setup-intent')
        return context


class SubscriptionView(generic.TemplateView):
    template_name = 'subscription.html'

    basic_price = 'price_1K1g64IlCeH6bP8RjH6yycp3'
    basic_img_src = 'basic_sunglasses.jpeg'

    premium_price = 'price_1K1g6eIlCeH6bP8RFlnFad9s'
    premium_img_src = 'premium_sunglasses.jpeg'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscription_item'] = {
            'price': self.basic_price, 'img': self.basic_img_src}
        return context

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        host = get_host(request)
        success_url = host + '/success?session_id={CHECKOUT_SESSION_ID}'
        session = stripe.checkout.Session.create(
            success_url=success_url,
            cancel_url=f'{host}/cancelled',
            mode='subscription',
            line_items=[{
                'price': request.POST['price_id'],
                'quantity': 1,
            }]
        )

        return HttpResponseRedirect(session.url)


class ManageSubscriptions(generic.TemplateView):
    template_name = 'manage_subscriptions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stripe.api_key = settings.STRIPE_SECRET_KEY

        configuration = stripe.billing_portal.Configuration.create(
            business_profile={
                'privacy_policy_url': 'https://example.com/privacy',
                'terms_of_service_url': 'https://example.com/terms',
            },
            features={
                'invoice_history': {
                    'enabled': True,
                },
                'payment_method_update': {
                    'enabled': True
                },
                "customer_update": {
                    "allowed_updates": [
                        "email",
                        "tax_id"
                    ],
                    "enabled": True
                },
                "subscription_cancel": {
                    "cancellation_reason": {
                        "enabled": True,
                        "options": ['too_expensive', 'unused', 'other']
                    },
                    "enabled": True,
                    "mode": "at_period_end",
                    "proration_behavior": "none"
                },
                "subscription_pause": {
                    "enabled": True
                },
                "subscription_update": {
                    "default_allowed_updates": [
                        'price', 'quantity',
                    ],
                    "enabled": True,
                    "products": [
                        {"prices": ['price_1K1g64IlCeH6bP8RjH6yycp3', 'price_1K1g6eIlCeH6bP8RFlnFad9s', 'price_1K1g2PIlCeH6bP8Rk4OI7UvU'],
                         # <- Product ID does not match Customer's subscription
                         'product': 'prod_Kh4Eia4pskgFxc'
                         }
                    ]
                }
            }
        )
        context['portal_config'] = configuration
        return context

    def post(self, request, *ags, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        customer = get_customer()
        config_id = request.POST['config_id']
        host = get_host(request)
        session = stripe.billing_portal.Session.create(
            customer=customer['id'],
            configuration=config_id,
            return_url=host
        )
        logger.info(session)
        logger.info(config_id)
        return HttpResponseRedirect(session.url)


class CheckoutLink(generic.TemplateView):
    template_name = 'checkout_link.html'


class InvoiceView(generic.TemplateView):
    template_name = 'invoices.html'
    customer = 'cus_KgfkGWhkAYC3ND'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        context['prices'] = list(
            filter(lambda p: p['recurring'] == None, stripe.Price.list(limit=100)))
        return context

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        price_id = request.POST.get('price_id', False)
        if price_id:
            stripe.InvoiceItem.create(
                customer=self.customer,
                price=price_id
            )
            stripe.Invoice.create(
                customer=self.customer,
                auto_advance=False,
                collection_method='send_invoice',
                days_until_due=30
            )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class CheckoutView(generic.TemplateView):
    template_name = 'checkout.html'
    price_type = 'subscription'

    def price_list_filter(self, price):
        if self.price_type == 'subscription':
            result = price['recurring'] != None
        else:
            result = price['recurring'] == None
        return result

    def get_context_data(self, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        context = super().get_context_data(**kwargs)
        context["prices"] = list(
            filter(
                self.price_list_filter,
                stripe.Price.list(limit=100)
            )
        )
        context["customers"] = list(
            stripe.Customer.list(limit=100)
        )
        return context

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            if request.POST.get('action') and request.POST['action'] == 'create-subscription':
                sub_kwargs = {
                    'customer': request.POST['customer'],
                    'items': [{
                        'price': request.POST['price']
                    }],
                    'payment_behavior': 'default_incomplete',
                    # 'payment_behavior': 'allow_incomplete',
                    'expand': ['latest_invoice.payment_intent'],
                }
                subscription = stripe.Subscription.create(**sub_kwargs)
                return JsonResponse(
                    {
                        'subscription_id': subscription.id,
                        'client_secret': subscription.latest_invoice.payment_intent.client_secret
                    }
                )
        except Exception as e:
            raise Exception(e)


class SubPaymentInfo(generic.TemplateView):
    template_name = 'payment_info.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        logger.info(pprinter(request.META))
        # logger.info(response.__dict__)
        return response


class OldSubscriptionView(generic.TemplateView):
    """
    Handling subscription processing using a somewhat outdated methd
    https://stripe.com/docs/billing/subscriptions/fixed-price

    """
    template_name = 'old_subscription.html'

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        email = request.POST.get('email', False)

        if email:
            try:
                customer = stripe.Customer.create(
                    email=email,
                    description='Old Subscription Flow'
                )
                return JsonResponse(customer)
            except Exception as e:
                raise e


# ---------------------------------------------------------------------------
#                       FUNCTION BASED VIEWS
# https://docs.djangoproject.com/en/3.2/topics/http/views/
# ---------------------------------------------------------------------------


def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = get_host(request)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url +
                "/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + '/cancelled/',
                payment_method_types=['card'],
                mode='subscription',
                shipping_address_collection={
                    'allowed_countries': ['US', 'CA'],
                },
                billing_address_collection='required',
                line_items=[
                    {
                        'price': 'price_1K2OgHIlCeH6bP8RWtxwQXpm',
                        'quantity': 1,
                        'adjustable_quantity': {
                            'enabled': True,
                            'minimum': 1,
                            'maximum': 10,
                        },
                    }
                ],
                automatic_tax={
                    'enabled': True
                },
                allow_promotion_codes=True,
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@ csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoit_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    # Validating webhook payload vai Stripe signature
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        # Using official library to construct event from payload
        # this includes verifying the webhook signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoit_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event.get('type', '') == 'checkout.session.completed':
        print('Payment was successful')

    return HttpResponse(status=200)


@ csrf_exempt
def webhook2(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoit_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body  # Need to get the raw body, not json()
    # Validating webhook payload vai Stripe signature

    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoit_secret
        )

    except ValueError as e:
        print('Invalid payload ', str(e))
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError as e:
        print('Invalid Stripe signature: ', str(e))
        return HttpResponse(status=400)

    etype = event.get('type', '')
    if etype.startswith('account'):
        print_event(msg='An account event has occurred', data=event)

    elif etype.startswith('charge.dispute'):
        print_event(msg="CHARGE DISPUTE EVENT! HOLY CRAP!", data=event)

    elif etype == 'charge.succeeded':
        print_event(msg='A charge event has succeeded', data=event)

    elif etype.startswith('checkout'):
        print_event(msg='A checkout event has occurredd', data=event)

    elif etype == 'payment_intent.created':
        print_event(msg='A payment_intent event has been created',
                    data=event['data'])

    elif etype == 'payment_intent.confirmed':
        print_event(msg='A payment_intent event has been confirmed',
                    data=event['data'])

    elif etype == 'payment_intent.canceled':
        print_event(msg='A payment_intent event has been canceled',
                    data=event['data'])

    elif etype == 'customer.created':
        print_event(msg='New Customer Created', data=event)
        cust = event['data']['object']
        models.Customer.objects.get_or_create(
            id=cust['id'],
            defaults={'data': cust}
        )

    elif etype == 'customer.updated':
        cust = event['data']['object']
        logger.info(f'Customer {cust["name"]} updated')
        models.Customer.objects.filter(id=cust['id']).update(data=cust)

    elif etype == 'checkout.session.completed':
        logger.info(
            f'Checkout Payment is successful and subscription created:\n{event}')

    elif etype == "invoice.created":
        pass
        # invoice = event['data']['object']
        # item = stripe.InvoiceItem.create(
        #     customer=invoice['customer'],
        #     price='price_1K3mDvIlCeH6bP8R43lTj74i',  # Price for stuff...pricey stuff
        #     invoice=invoice['id']
        # )
        # logger.info(f'InvoiceItem added to newly created invoice: {item}')

    elif etype == "invoice.payment_succeeded":
        data_object = event['data']['object']
        if data_object['billing_reason'] == 'subscription_create':
            subscription_id = data_object['subscription']
            payment_intent_id = data_object['payment_intent']

            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            stripe.Subscription.modify(
                subscription_id,
                default_payment_method=payment_intent.payment_method
            )

    elif etype.startswith('invoice.') and etype != "invoice.created":
        invoice = event['data']['object']
        status = invoice["status"]
        logger.info(f'An invoice with status {status} was received')
        # if status == "draft":
        #     stripe.Invoice.finalize_invoice(invoice['id'])
        #     logger.info(f'Invoice {invoice["id"]} finalized')
        # elif status == "open":
        #     stripe.Invoice.pay(invoice['id'])
        #     logger.info(f'Invoice {invoice["id"]} paid')
        # else:
        print_event(msg="Stuff happened with an invoice", data=event)

    elif etype == 'payment_method.created':
        print_event(msg='New Payment Method Created', data=event)

    return HttpResponse(status=200)


def host_apple_stuff(request):
    fpath = Path(settings.BASE_DIR, 'payments',
                 'files/apple-developer-merchantid-domain-association')
    logger.info(fpath)
    f = open(fpath)
    content = f.read()
    f.close()

    return HttpResponse(content, content_type='text/plain')
