from django.db import models
from django.core.serializers.json import DjangoJSONEncoder


class PaymentIntent(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    data = models.JSONField(encoder=DjangoJSONEncoder, null=True)


class Customer(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    data = models.JSONField(encoder=DjangoJSONEncoder, null=True)


class Dispute(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    data = models.JSONField(encoder=DjangoJSONEncoder, null=True)
