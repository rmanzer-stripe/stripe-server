"""
A specific set of namespaced API views used to handle the back-end for Supermanzer Software Consulting.
"""
from datetime import datetime, timedelta
import pdb
import stripe

from rest_framework.response import Response
from rest_framework import viewsets

from rest_framework.decorators import action, api_view
from .api_views import RequestKwargs

SUPERMANZER_API_KEY = 'sk_test_51K9BjQKyzYDRNndd5mZKva9iqMx7EPsi4qoS4v48c2LwyTrUMsUZP7oj3D5erA3jFGiXYjNqnkrCGG3naLrKfEN100HdrNoJCv'
# stripe.api_key = SUPERMANZER_API_KEY
# stripe.api_version = '2023-10-16'


class PriceViewSet(viewsets.ViewSet):
    def list(self, request):
        stripe.api_key = SUPERMANZER_API_KEY
        prices = stripe.Price.list(expand=['data.product'])
        return Response(prices)


class CustomerViewSet(viewsets.ViewSet, RequestKwargs):
    REQUIRED_KWARGS = ['email']
    API_KWARGS = [
        'address',
        'description',
        'email',
        'metadata',
        'name',
        'payment_method',
        'phone',
        'shipping',
        'balance',
        'cash_balance',
        'coupon',
        'invoice_prefix',
        'invoice_settings',
        'next_invoice_sequence',
        'preferred_locales',
        'promotion_code',
        'source',
        'tax',
        'tax_exempt',
        'tax_id_data',
        'test_clock'
    ]

    def list(self, request):
        stripe.api_key = SUPERMANZER_API_KEY
        customers = stripe.Customer.list()
        return Response(customers)

    def create(self, request):
        stripe.api_key = SUPERMANZER_API_KEY
        customer = stripe.Customer.create(**self.get_kwargs(request))
        return Response(customer)

    def retrieve(self, request, pk=None):
        stripe.api_key = SUPERMANZER_API_KEY
        customer = stripe.Customer.retrieve(pk)
        return Response(customer)

    def update(self, request, pk=None):
        stripe.api_key = SUPERMANZER_API_KEY
        kwargs = self.get_kwargs(request)
        customer = stripe.Customer.modify(pk, **kwargs)
        return Response(customer)


class QuoteViewSet(viewsets.ViewSet):
    def create(self, request):
        stripe.api_key = SUPERMANZER_API_KEY
        email = request.data.get('email')
        line_items = request.data.get('line_items')
        if not all([email, line_items]):
            return Response({'error': 'Missing required parameters'})

        customer = stripe.Customer.list(email=email)
        if customer:
            customer = customer['data'][0]
        else:
            customer = stripe.Customer.create(email=email)

        quote = stripe.Quote.create(
            customer=customer['id'],
            line_items=line_items
        )
        exipry = int((datetime.now() + timedelta(days=7)).timestamp())
        quote = stripe.Quote.finalize_quote(quote['id'], expires_at=exipry)
        return Response(quote)

    @action(detail=True, methods=['get'])
    def get_pdf(sel, request, pk=None):
        stripe.api_key = SUPERMANZER_API_KEY
        quote = stripe.Quote.retrieve(pk)
        if not quote:
            return Response({'error': 'Quote not found'})
        quote = stripe.Quote.pdf(pk)
        return Response(quote)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        stripe.api_key = SUPERMANZER_API_KEY
        quote = stripe.Quote.retrieve(pk)
        if not quote:
            return Response({'error': 'Quote not found'})
        quote = stripe.Quote.accept(pk)
        return Response(quote)
