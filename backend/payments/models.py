
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder


class StripeAccount(models.Model):
    """
    Defining DB records for stand-alone Stripe Accounts.  

    These are used to switch the context and API keys used to instantiate Stripe libraries. 
    """
    COUNTY_CHOICES = (
        ('US', 'United States of America'),
        ('CA', 'Canada'),
        ('MX', 'Mexico'),
        ('DE', "Germany"),
        ('FR', 'France'),
    )
    account_id = models.CharField(
        max_length=255, null=True, blank=True, help_text='Account ID from Stripe')
    test_private_api_key = models.CharField(
        max_length=255, null=True, blank=True, name='Test Private Key', help_text='Test mode server-side API key')
    test_public_api_key = models.CharField(
        max_length=255, null=True, blank=True, name='Test Public Key', help_text='Test mode client-side API key')
    live_private_api_key = models.CharField(
        max_length=255, null=True, blank=True, name='Live Private Key', help_text='Live mode server-side API key')
    live_public_api_key = models.CharField(
        max_length=255, null=True, blank=True, name='Live Public Key', help_text='Live mode client-side API key')
    name = models.CharField(max_length=60, null=True, blank=True,
                            help_text='Friendly name for this account')
    country = models.CharField(
        max_length=2, choices=COUNTY_CHOICES, null=True, blank=True, help_text='ISO 2-letter abbreviation for country')
    has_connect = models.BooleanField(
        help_text='Whether this account is a platform with Connect Accounts associated')

    def __str__(self) -> str:
        return self.name


class PaymentIntent(models.Model):
    OFF_SESSION = 'off_session'
    ON_SESSION = 'on_session'
    FUTURE_USAGE_CHOICES = [
        (OFF_SESSION, 'off session'),
        (ON_SESSION, 'on session')
    ]
    id = models.CharField(max_length=255, primary_key=True)
    data = models.JSONField(encoder=DjangoJSONEncoder, null=True)
    amount = models.BigIntegerField(null=True)
    automatic_payment_methods = models.JSONField(
        encoder=DjangoJSONEncoder, null=True)
    charges = models.JSONField(encoder=DjangoJSONEncoder, null=True)
    client_secret = models.CharField(max_length=255, null=True)
    currency = models.CharField(max_length=3, null=True)
    customer = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    last_payment_error = models.JSONField(encoder=DjangoJSONEncoder, null=True)
    metadata = models.JSONField(encoder=DjangoJSONEncoder, null=True)
    next_action = models.JSONField(encoder=DjangoJSONEncoder, null=True)
    payment_method = models.CharField(max_length=255, null=True)
    payment_method_types = models.JSONField(
        encoder=DjangoJSONEncoder, null=True)
    receipt_email = models.CharField(max_length=200, null=True)
    setup_future_usage = models.CharField(
        max_length=15, choices=FUTURE_USAGE_CHOICES, null=True)
    shipping = models.JSONField(encoder=DjangoJSONEncoder, null=True)
    statement_descriptor = models.CharField(max_length=255, null=True)
    statement_descriptor_suffix = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=30, null=True)
    stripe_account = models.ForeignKey(
        to=StripeAccount, on_delete=models.SET_NULL, related_name='payment_intents', null=True)

    def update_from_data(self):
        """
        Unroll record info stored in `data` field into corresponding model fields
        """
        update_kwargs = {
            f.name: self.data.get(f.name)
            for f in self._meta.fields
            if self.data.get(f.name, False)
        }
        change = self._meta.model.objects.filter(
            id=self.id).update(**update_kwargs)
        return change

    class Meta:
        ordering = ['-data__created']


class Customer(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    data = models.JSONField(encoder=DjangoJSONEncoder, null=True)
    stripe_account = models.ForeignKey(
        to=StripeAccount, null=True, on_delete=models.SET_NULL, related_name='customers')

    class Meta:
        ordering = ['-data__created']


class Dispute(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    data = models.JSONField(encoder=DjangoJSONEncoder, null=True)

    class Meta:
        ordering = ['-data__created']


class Charge(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    data = models.JSONField(encoder=DjangoJSONEncoder, null=True)

    class Meta:
        ordering = ['-data__created']


class Invoice(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    data = models.JSONField(encoder=DjangoJSONEncoder, null=True)

    class Meta:
        ordering = ['-data__created']


class SetupIntent(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    data = models.JSONField(encoder=DjangoJSONEncoder, null=True)

    class Meta:
        ordering = ['-data__created']


class Price(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    data = models.JSONField(encoder=DjangoJSONEncoder, null=True)

    class Meta:
        ordering = ['-data__created']


class Product(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    data = models.JSONField(encoder=DjangoJSONEncoder, null=True)

    class Meta:
        ordering = ['-data__created']


class Subscription(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    data = models.JSONField(encoder=DjangoJSONEncoder, null=True)

    class Meta:
        ordering = ['-data__created']


class Account(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    data = models.JSONField(encoder=DjangoJSONEncoder, null=True)

    class Meta:
        ordering = ['-data__created']


class AppAccount(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    data = models.JSONField(encoder=DjangoJSONEncoder, null=True)

    class Meta:
        ordering = ['-data__created']


class Location(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    data = models.JSONField(encoder=DjangoJSONEncoder, null=True)

    class Meta:
        ordering = ['-data__created']


class Reader(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    data = models.JSONField(encoder=DjangoJSONEncoder, null=True)

    class Meta:
        ordering = ['-data__created']


class Order(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    data = models.JSONField(encoder=DjangoJSONEncoder, null=True)

    class Meta:
        ordering = ['-data__created']


class Coupon(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    data = models.JSONField(encoder=DjangoJSONEncoder, null=True)

    class Meta:
        ordering = ['-data__created']


class PromotionCode(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    data = models.JSONField(encoder=DjangoJSONEncoder, null=True)

    class Meta:
        ordering = ['-data__created']


class TestClock(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    data = models.JSONField(encoder=DjangoJSONEncoder, null=True)

    class Meta:
        ordering = ['-data__created']


class TaxRate(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    data = models.JSONField(encoder=DjangoJSONEncoder, null=True)

    class Meta:
        ordering = ['-data__created']


class PaymentMethodDomain(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    data = models.JSONField(encoder=DjangoJSONEncoder, null=True)

    class Meta:
        ordering = ['-data__created']
