from django.db import models
from django.core.serializers.json import DjangoJSONEncoder


class PaymentItent(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    data = models.JSONField(encoder=DjangoJSONEncoder, null=True)
