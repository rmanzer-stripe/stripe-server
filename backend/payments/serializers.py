"""
    payments/serializers.py
    
    Define how application data should be serialized into JSON
    https://www.django-rest-framework.org/api-guide/serializers/
"""
from rest_framework import serializers

from payments import models


class StripeObjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = None
        fields = ['id', 'data']


class CustomerSerializer(StripeObjectSerializer):
    class Meta:
        model = models.Customer
        fields = StripeObjectSerializer.Meta.fields


class DisputeSerializer(StripeObjectSerializer):
    class Meta:
        model = models.Dispute
        fields = StripeObjectSerializer.Meta.fields


class EvidenceSerializer(serializers.Serializer):
    dispute_id = serializers.CharField(max_length=255)
    evidence = serializers.CharField(max_length=255)


class PaymentIntentSerializer(StripeObjectSerializer):
    class Meta:
        model = models.PaymentIntent
        fields = ['id', 'data']


class ChargeSerializer(StripeObjectSerializer):
    class Meta:
        model = models.Charge
        fields = StripeObjectSerializer.Meta.fields


class InvoiceSerializer(StripeObjectSerializer):
    class Meta:
        model = models.Invoice
        fields = StripeObjectSerializer.Meta.fields


class SetupIntentSerializer(StripeObjectSerializer):
    class Meta:
        model = models.SetupIntent
        fields = StripeObjectSerializer.Meta.fields


class SubscriptionSerializer(StripeObjectSerializer):
    class Meta:
        model = models.Subscription
        fields = StripeObjectSerializer.Meta.fields


class PriceSerializer(StripeObjectSerializer):
    class Meta:
        model = models.Price
        fields = StripeObjectSerializer.Meta.fields


class ProductSerializer(StripeObjectSerializer):
    class Meta:
        model = models.Product
        fields = StripeObjectSerializer.Meta.fields


class ReaderSerializer(StripeObjectSerializer):
    class Meta:
        model = models.Reader
        fields = StripeObjectSerializer.Meta.fields


class OrderSerializer(StripeObjectSerializer):
    class Meta:
        model = models.Order
        fields = ['data']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StripeAccount
        fields = '__all__'


class ConnectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Account
        fields = '__all__'


class AppAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AppAccount
        fields = ['id']


class TestClockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TestClock
        fields = '__all__'


class TaxRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaxRate
        fields = '__all__'


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentMethodDomain
        fields = '__all__'
