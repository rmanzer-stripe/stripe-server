import stripe
import pprint
import logging
import json

from pathlib import Path

from django.views import generic
from django.conf import settings
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy


from payments.forms import EvidenceForm
from payments import models


printer = pprint.PrettyPrinter(indent=4)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger.info('Setting up payment intent')
        stripe.api_key = settings.STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.create(
            amount=14000,
            currency='usd',
            metadata={'integration_check': 'accept_a_payment'}
        )
        context['client_secret'] = intent.client_secret
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

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
            automatic_payment_methods={'enabled': True}
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


def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url +
                "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'T-shirt',
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': 2000,
                    }
                ]
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

    return HttpResponse(status=200)


def host_apple_stuff(request):
    fpath = Path(settings.BASE_DIR, 'payments',
                 'files/apple-developer-merchantid-domain-association')
    logger.info(fpath)
    f = open(fpath)
    content = f.read()
    f.close()

    return HttpResponse(content, content_type='text/plain')
