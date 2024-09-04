import stripe

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings

from logging import getLogger

logger = getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(["GET"])
def get_publishable_key(request):
    """
    Fetch the current publisbable key from the server

    Avoid hard-coding like the plague
    """
    return Response({"publishable_key": settings.STRIPE_PUBLISHABLE_KEY})


@api_view(["GET"])
def get_custom_si(request):
    customer = 'cus_KpJotPZRDgVRvy'
    si = stripe.SetupIntent.create(
        customer=customer,
        payment_method_types=['card']
    )
    return Response({'setup_intent': si})


@api_view(["POST"])
def payment_sheet(request):
    customer = stripe.Customer.create()
    ephemeralKey = stripe.EphemeralKey.create(
        customer=customer['id'],
        stripe_version='2020-08-27',
    )
    paymentIntent = stripe.PaymentIntent.create(
        amount=1099,
        currency='eur',
        customer=customer['id'],
        automatic_payment_methods={
            'enabled': True,
        },
    )
    resp = {
        'paymentIntent': paymentIntent.client_secret,
        'ephemeralKey': ephemeralKey.secret,
        'customer': customer.id,
        'publishableKey': settings.STRIPE_PUBLISHABLE_KEY
    }
    return Response(resp)


class WebhookView(APIView):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        print(">>>>", request.data)
        return Response(status=200)
