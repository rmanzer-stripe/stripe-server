"""
    payments/api_views.py

    Define DRF Viewsets for Payments operations
    https://www.django-rest-framework.org/api-guide/viewsets/

    > After routing has determined which controller to use for a request,
    > your controller is responsible for making sense of the request and
    > producing the appropriate output.
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta
import json
from locale import currency
import re
from urllib.request import Request
import stripe
from stripe import ErrorObject
import uuid

from django.conf import settings
from django.db.models import Q


from rest_framework.response import Response
from rest_framework import viewsets

from rest_framework.decorators import action, api_view


from payments import models
from payments import serializers

from logging import getLogger


logger = getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

account_keys_dict = {
    "acct_1O83hCB9iVsTMEuJ": "sk_test_51O83hCB9iVsTMEuJ5k6rGiWrzj0POCOicyZn4yP7azXCgVrZ7E4NsomALOruGOxUJY4lBlY1rDEvj9MaV79o8oIP00rhsR7iKD",  # British Manzer
    "acct_1PMeTpL3oXCU477z": "sk_test_51PMeTpL3oXCU477zPhhEHy4lMWXi6d7vBUMgAE27tLnRa3S6lwOhSL7id64YSC4VsDQ86M7u0alrdRBsDgrz4JpY00p8o3mptS",  # French Manzer
    "acct_1JticYIlCeH6bP8R": "sk_test_51JticYIlCeH6bP8RQmkScSIBs4Gg870ecW5lRX02YE1O3m7HpPbUHfPTc22MS98LXEaXwuK9yzp8L6cDd3O4qs02002fcAA5TZ",  # Default test account
    "acct_1Ppek1Q6JWPgQcCn": "sk_test_51Ppek1Q6JWPgQcCnyLHdzTsI8E6mt7KfYoB0bHmfAjGf3fYuhxKfEqZleJCQYOhNPROgWmBPfqLf2HCFUtojaC1o002Ro5Tp2z",  # First sandbox account
    "acct_1PnNzpIWHOnXaRR4": "sk_test_51PnNzpIWHOnXaRR4QHVarFVlwG37edvefNAQ55gWOY6kooetjGC2SfjkpGuSzLCfjKy0fli0jODQahCSHi1s6WFt00D8eGHDpW",  # Default sandbox account
}


@dataclass
class Person:
    """
    Create a data transfer object representing a person
    """

    name: str
    email: str
    phone_nummber: str


class RequestKwargs:
    REQUIRED_KWARGS = []  # overwritten in subcless
    API_KWARGS = []  # overwritten in subclass

    def get_kwargs(self, request, skip_required=False) -> dict:
        """
        Create keyword arguments dictionary from parameters in request

        Args:
            request (HttpRequest): The request to this API

        Raises:
            AttributeError: If any of the required kwargs (defined in subclasses) are missing from the request or API_KWARGS are undefined on the subclass

        Returns:
            dict: Dictionary of keyword arguments (kwargs) for a Stripe Python library request
        """
        #
        if not bool(self.API_KWARGS):
            raise AttributeError(
                "API_KWARGS empty.  \
                    Subclasses of RequestKwargs must specify API_KWARGS list"
            )

        data = request.data
        query_params = request.query_params
        kwargs = {}
        if bool(data):
            has_required = all(
                [rk in request.data.keys() for rk in self.REQUIRED_KWARGS]
            )

            if not has_required and not skip_required:
                logger.error(f"Missing required kwargs {self.REQUIRED_KWARGS}")
                raise AttributeError(
                    f"Request is missing one or more required kwargs: {self.REQUIRED_KWARGS}"
                )
            logger.info(f"Request data keys: {request.data.keys()}")
            logger.info(f"API KWARGS: {self.API_KWARGS}")

            kwargs = {
                kw: request.data.get(kw)
                for kw in self.API_KWARGS
                if kw in request.data.keys()
            }
            if "mandate_data" in request.data.keys():
                mandate = request.data.get("mandate_data")
                mandate["customer_acceptance"].update(
                    {
                        "online": {
                            "ip_address": request.META.get("REMOTE_ADDR"),
                            "user_agent": request.META.get("HTTP_USER_AGENT"),
                        }
                    }
                )
                kwargs["mandate_data"] = mandate
        elif bool(query_params):
            logger.info(f"Query params: {query_params}")
            new_params = {}
            for k, v in query_params.items():
                if k.endswith("[]"):
                    new_params[k[:-2]] = v.split(",")
                else:
                    # query params come in as strings, so we need to convert them to the correct type
                    new_params[k] = json.loads(v) if v.startswith("{") else v

            kwargs = {
                kw: new_params.get(kw)
                for kw in self.API_KWARGS
                if kw in new_params.keys()
            }
            logger.info(f"New params: {new_params}")
        return kwargs

    def get_client(self, request):
        """
        Get the client object for the request
        """
        account = request.data.get("account", None)
        if account is not None:
            return stripe.StripeClient(api_key=account_keys_dict[account])
        else:
            # Specifying default test account
            account = "acct_1JticYIlCeH6bP8R"
            return stripe.StripeClient(api_key=account_keys_dict[account])


class FilterQueryset:

    def cast_values(self, v):
        new_v = None
        bool_dict = {"True": True, "False": False}
        if v in bool_dict.keys():
            new_v = bool_dict[v]
        else:
            try:
                new_v = int(v)
            except ValueError as e:
                new_v = v
        return new_v

    def get_filtered_queryset(self, request):
        print("getting filtered queryset")
        qs = self.get_queryset()
        filter_kwargs = {
            k: self.cast_values(v) for k, v in request.query_params.items()
        }
        print(filter_kwargs)
        return qs.filter(**filter_kwargs)


class ProductViewSet(viewsets.ModelViewSet, RequestKwargs):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    REQUIRED_KWARGS = ["name"]
    API_KWARGS = [
        "id",
        "name",
        "active",
        "description",
        "metadata",
        "image",
        "package_dimensions",
        "shippable",
        "statement_descriptor",
        "tax_code",
        "unit_label",
        "url",
    ]

    def create(self, request, *args, **kwargs):
        kwargs = self.get_kwargs(request)
        product = stripe.Product.create(**kwargs)
        return Response(data={"product": product}, status=200)

    @action(detail=True, methods=["GET"])
    def default_price(self, request, pk=None):
        product = models.Product.objects.get(id=pk)
        default_price_id = product.data["default_price"]
        price = models.Price.objects.get(id=default_price_id).data
        return Response(data=price, status=200)


class PriceViewSet(viewsets.ModelViewSet, RequestKwargs):
    queryset = models.Price.objects.all()
    serializer_class = serializers.PriceSerializer
    search_fields = ["data__product", "data__metadata", "data__nickname"]

    REQUIRED_KWARGS = ["currency", "unit_amount", "product"]
    API_KWARGS = REQUIRED_KWARGS + [
        "active",
        "billing_scheme",
        "lookup_key",
        "metadata",
        "nickname",
        "recurring",
        "tax_behavior",
        "tiers",
        "tiers_mode",
        "transform_quantity",
        "usage_type",
        "currency_options",
        "custom_unit_amount",
        "transform_quantity",
        "unit_amount_decimal",
    ]

    def create(self, request, *args, **kwargs):
        kwargs = self.get_kwargs(request)
        price = stripe.Price.create(**kwargs)
        return Response(data={"price": price}, status=200)

    @action(detail=False, methods=["GET"])
    def recurring(self, request):
        """
        Get all recurring prices
        """
        kwargs = {"data__type": "recurring"}
        usage_type = request.query_params.get("usage_type", None)
        if usage_type:
            kwargs["data__recurring__usage_type"] = usage_type
        prices = models.Price.objects.filter(**kwargs).values("data")
        return Response(data={"prices": prices}, status=200)

    @action(detail=False, methods=["GET"])
    def filter_currency(self, request):
        """
        Filter prices by currency
        """
        currency = request.query_params.get("currency", None)

        if currency:
            prices = models.Price.objects.filter(
                data__currency=currency
            ).values("data")

            return Response(data=prices, status=200)
        else:
            return Response(data={"msg": "No currency provided"}, status=400)

    def list(self, request):
        """
        List all prices
        """
        kwargs = self.get_kwargs(request)
        logger.info(f"Request kwargs: {kwargs}")
        # TODO: This doesn't work, fix it
        prices = stripe.Price.list(**kwargs)
        logger.info(f"Prices: {prices}")
        # data = self.serializer_class(prices, many=True).data
        return Response(data={"prices": prices}, status=200)


class CustomerViewSet(viewsets.ModelViewSet, RequestKwargs):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    search_fields = ["data__name", "data__email"]

    REQUIRED_KWARGS = []
    API_KWARGS = [
        "address",
        "description",
        "email",
        "metadata",
        "name",
        "payment_method",
        "phone",
        "shipping",
        "balance",
        "cash_balance",
        "coupon",
        "invoice_prefix",
        "invoice_settings",
        "next_invoice_sequence",
        "preferred_locales",
        "promotion_code",
        "source",
        "tax",
        "tax_exempt",
        "tax_id_data",
        "test_clock",
    ]

    def check_and_attach(self, customer, params):
        if not customer.invoice_settings.default_payment_method and params.get(
            "invoice_settings", {}
        ).get("default_payment_method", False):
            pm_id = params["invoice_settings"]["default_payment_method"]
            stripe.PaymentMethod.attach(pm_id, customer=customer.id)
            stripe.Customer.modify(
                customer.id, invoice_settings=params["invoice_settings"]
            )
            return True

    def create(self, request):
        kwargs = self.get_kwargs(request)
        # Use a Get or Create pattern
        customers = stripe.Customer.list(email=kwargs["email"])
        if len(customers) > 0:
            customer = customers.data[0]
            stripe.Customer.modify(customer.id, **kwargs)
            self.check_and_attach(customer, kwargs)
        else:
            customer = stripe.Customer.create(**kwargs)
        return Response(data={"customer": customer}, status=200)

    def list(self, request):
        kwargs = self.get_kwargs(request)
        client = self.get_client(request)
        logger.info(f"Request kwargs: {kwargs}")
        customers = client.customers.list(kwargs)
        return Response(data={"customers": customers}, status=200)

    def retrieve(self, request, pk=None):
        kwargs = self.get_kwargs(request)
        customer = stripe.Customer.retrieve(pk, **kwargs)
        return Response(data=customer, status=200)

    @action(detail=True, methods=["post"])
    def fund_cash_balance(self, request, pk=None):
        cust = self.get_object()
        amount_to_fund = request.data.get("amount", None)
        currency = request.data.get("currency", None)
        if not all([amount_to_fund, currency]):
            raise AttributeError(
                f"Request is missing one or more required kwargs: amount, currency"
            )
        cb = stripe.Customer.TestHelpers.fund_cash_balance(
            cust.id, amount=amount_to_fund, currency=currency
        )
        return Response(data={"cash_balance": cb}, status=200)

    @action(detail=True, methods=["post"])
    def get_ephemeral_key(self, request, pk=None):
        key = stripe.EphemeralKey.create(
            customer=pk, stripe_version=settings.STRIPE_API_VERSION
        )
        return Response(data=key.secret, status=200)

    @action(detail=True, methods=["post"])
    def create_session(self, request, pk=None):
        session = stripe.CustomerSession.create(
            customer=pk,
            components={
                "payment_element": {
                    "enabled": True,
                    "features": {
                        "payment_method_save": "enabled",
                        "payment_method_save_usage": "off_session",
                    },
                }
            },
        )
        return Response(data={"session": session}, status=200)

    @action(detail=False, methods=["post"])
    def get_or_create_mobile_customer(self, request):
        """
        Get or create a customer from mobile device
        """
        try:
            kwargs = self.get_kwargs(request)
            name = kwargs.get("name", "Mobile")
            email = kwargs.get("email", "mobile@example.com")
            customer = stripe.Customer.list(email=email)
            if len(customer) > 0:
                customer = customer.data[0]
            else:
                customer = stripe.Customer.create(name=name, email=email)
            return Response(data={"customer": customer}, status=200)
        except Exception as e:
            return Response(data={"msg": str(e)}, status=500)


class PaymentMethodViewSet(viewsets.ViewSet, RequestKwargs):
    REQUIRED_KWARGS = ["type"]
    API_KWARGS = [
        "billing_details",
        "metadata",
        "acss_debit",
        "affirm",
        # TODO: Add more
    ]

    @action(detail=True, methods=["post"])
    def attach_pm(self, request, pk=None):
        response = Response(data={"msg": "Failed to attach"}, status=500)
        customer = request.data.get("customer", None)
        if customer is not None and type(pk) == str:
            pm = stripe.PaymentMethod.attach(
                pk, customer=customer  # type: ignore
            )
            response = Response(
                data={"msg": "payment method attached"}, status=200
            )

        return response


class DisputeViewSet(viewsets.ModelViewSet):
    """
    Handles all Dispute related activites
    """

    queryset = models.Dispute.objects.all()
    serializer_class = serializers.DisputeSerializer
    search_fields = ["data__status", "data__reason"]

    @action(detail=True, methods=["post"])
    def provide_evidence(self, request, pk=None):
        serializer = serializers.EvidenceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        stripe.Dispute.modify(data["id"], evidence=data["evidence"])
        return Response(data={"message": "Success"}, status=200)


class PaymentIntentViewSet(viewsets.ModelViewSet, RequestKwargs):
    """
    Handle direct Payment Intent operations
    """

    queryset = models.PaymentIntent.objects.all()
    serializer_class = serializers.PaymentIntentSerializer
    # filter_fields = ['data__status', 'data__amount',
    #                  'data__currency']

    REQUIRED_KWARGS = ["amount", "currency"]
    API_KWARGS = [
        "amount",
        "currency",
        "payment_method_types",
        "payment_method_options",
        "capture_method",
        "payment_method",
        "confirm",
        "setup_future_usage",
        "automatic_payment_methods",
        "customer",
        "return_url",
        "mandate_data",
        "confirmation_token",
        "metadata",
    ]

    def generate_response(self, intent):
        if (
            intent.status == "requires_action"
            and intent.next_action.type == "use_stripe_sdk"
        ):
            # Tell the client to handle the action
            return Response(
                data={
                    "requires_action": True,
                    "payment_intent_client_secret": intent.client_secret,
                }
            )
        elif intent.status == "succeeded":
            return Response(data={"success": True}, status=200)
        elif intent.status == "requires_capture":
            return Response(
                data={
                    "message": "Your payment details have been captured and you will be billed later"
                }
            )
        else:
            return Response(
                data={"error": "Invalid PaymentIntent status"}, status=500
            )

    def get_queryset(self):
        qs = super().get_queryset()
        pi_status = self.request.query_params.get("status", False)
        exclude = self.request.query_params.get("exclude")
        if pi_status:
            if exclude is not None:
                qs = qs.filter(~Q(data__status=pi_status))
            else:
                qs = qs.filter(data__status=pi_status)
        return qs

    def retrieve(self, request, pk=None):
        intent = stripe.PaymentIntent.retrieve(pk, expand=["latest_charge"])
        return Response(intent)

    def create(self, request, *args, **kwargs):
        pi_kwargs = self.get_kwargs(request)
        client = self.get_client(request)
        try:
            intent = client.payment_intents.create(pi_kwargs)
            data, status = {"intent": intent}, 200
        except Exception as ex:
            err_dict = {
                "code": ex.error.code,
                "message": ex.error.message,
                "type": ex.error.type,
                "request": ex.request_id,
            }
            data, status = {"error": err_dict}, 400
        return Response(data=data, status=status)

    @action(detail=True, methods=["post"])
    def update_intent(self, request, pk=None):
        if not pk:
            return Response(
                data={"msg": "No PaymentIntent ID provided"}, status=400
            )
        update_kwargs = self.get_kwargs(request, skip_required=True)
        client = self.get_client(request)
        logger.info(f"Update kwargs: {update_kwargs}")
        try:
            updated_intent = client.payment_intents.update(pk, update_kwargs)
            return Response(data={"intent": updated_intent}, status=200)
        except Exception as e:
            return Response(data={"msg": str(e)}, status=500)

    @action(detail=False, methods=["post"])
    def hold(self, request):
        kwargs = self.get_kwargs(request, hold=True)
        intent = stripe.PaymentIntent.create(**kwargs)
        return self.generate_response(intent)

    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):
        client = self.get_client(request)
        intent = client.payment_intent.confirm(pk)
        return self.generate_response(intent)

    @action(detail=True, methods=["post"])
    def capture(self, request, pk=None):
        amount_to_capture = request.data.get("amount_to_capture")
        capture = request.data.get("capture", False)
        cancel = request.data.get("cancel", False)
        verb = "canceled" if cancel else "captured"
        try:
            if cancel:
                intent = stripe.PaymentIntent.cancel(pk)
            if capture:
                intent = stripe.PaymentIntent.capture(
                    pk, amount_to_capture=amount_to_capture
                )
            return Response(
                data={
                    "msg": f"Success. Payment Intent {intent.id} successfully {verb}"
                }
            )
        except Exception as e:
            return Response(data={"msg": str(e)}, status=500)

    @action(detail=True, methods=["post"])
    def refund(self, request, pk=None):
        action = request.data.get("action")
        amount = request.data.get("amount", 0)
        resp_dict = {}
        try:
            if action == "refund":
                response = stripe.Refund.create(
                    amount=amount, payment_intent=pk
                )
                resp_dict["msg"] = (
                    f"Refund process returned status: {response.status}"
                )
            if action == "cancel":
                response = stripe.PaymentIntent.cancel(pk)
                resp_dict["msg"] = (
                    f"PaymentIntent cancel pross returned status: {response.status}"
                )
            status = 200
        except stripe.error.InvalidRequestError as e:
            resp_dict = {"msg": e.user_message}
            status = 500
        except Exception as e:
            resp_dict = {"msg": str(e)}
            status = 500

        return Response(data=resp_dict, status=status)

    @action(detail=True, methods=["POST"])
    def cancel(self, request, pk=None):
        result, status = {}, 200
        try:
            intent = stripe.PaymentIntent.cancel(pk)
            result["status"] = "Success"
            result["message"] = f"Payment Intent {intent.id} canceled"
        except Exception as ex:
            result["status"] = "Error"
            result["message"] = ex.error.message

        return Response(data=result, status=status)

    @action(detail=False, methods=["GET"])
    def needs_funding(self, request):
        """
        Get all Payment Intents that need funding
        """
        pi_list = models.PaymentIntent.objects.filter(
            data__status="requires_action",
            data__payment_method_types=["customer_balance"],
        )
        pi_list = self.serializer_class(pi_list, many=True).data
        return Response(data=pi_list, status=200)

    @action(detail=False, methods=["POST"])
    def default(self, request):
        params = {
            "amount": 2599,
            "currency": "USD",
            "automatic_payment_methods": {"enabled": True},
        }
        intent = stripe.PaymentIntent.create(**params)
        return Response(data=intent.client_secret, status=200)

    def validate_conf_token(self, token):
        banned_states = ["FL", "TX", "TN", "SC", "GA"]
        conf_token = stripe.ConfirmationToken.retrieve(token)
        logger.info(f"Confirmation token: {conf_token}")
        if conf_token.shipping.address.state in banned_states:
            raise ValueError(
                f"Shipping to {conf_token.shipping.address.state} is not allowed"
            )

    @action(detail=False, methods=["POST"])
    def create_confirm(self, request):
        params = self.get_kwargs(request)
        try:
            self.validate_conf_token(params["confirmation_token"])
            intent = stripe.PaymentIntent.create(**params)
            return Response(data={"intent": intent}, status=200)
        except Exception as e:
            return Response(data={"error": json.dumps(e)}, status=500)


class CheckoutSessionViewSet(viewsets.ViewSet, RequestKwargs):

    REQUIRED_KWARGS = ["mode"]
    API_KWARGS = [
        "cancel_url",
        "mode",
        "success_url",
        "client_reference_id",
        "currency",
        "customer",
        "customer_email",
        "line_items",
        "metadata",
        "payment_method_types",
        "after_expiration",
        "allow_promotion_codes",
        "automatic_tax",
        "billing_address_collection",
        "consent_collection",
        "custom_text",
        "custom_fields",
        "customer_creation",
        "customer_update",
        "discounts",
        "expires_at",
        "locale",
        "payment_intent_data",
        "shipping_address_collection",
        "shipping_options",
        "submit_type",
        "subscription_data",
        "tax_id_collection",
        "ui_mode",
        "return_url",
        "saved_payment_method_options",
        "payment_method_data",
        "payment_method_options",
    ]

    def create(self, request, *args, **kwargs):
        logger.info(f"Request data keys: {request.data.keys()}")
        checkout_kwargs = self.get_kwargs(request)
        try:
            session = stripe.checkout.Session.create(**checkout_kwargs)
            return Response(data={"url": session.url}, status=200)
        except Exception as ex:
            return Response(data={"error": str(ex)}, status=400)

    def retrieve(self, request, pk=None):
        session = stripe.checkout.Session.retrieve(pk)
        return Response(data={"session": session}, status=200)

    @action(detail=False, methods=["post"])
    def create_embedded(self, request, *args, **kwargs):
        checkout_kwargs = self.get_kwargs(request)
        try:
            session = stripe.checkout.Session.create(**checkout_kwargs)
            resp = Response(data={"secret": session.client_secret}, status=200)
        except Exception as ex:
            resp = Response(data={"error": str(ex)}, status=400)
        # Reset API version
        return resp


class ChargeViewSet(viewsets.ModelViewSet):
    queryset = models.Charge.objects.all()
    serializer_class = serializers.ChargeSerializer

    def handle_customer(self, request):
        cust_id = request.data.get("customer_id", False)
        cust_name = request.data.get("customer_name", False)
        token = request.data.get("stripeToken", False)
        msg = None
        if token:
            if cust_id:
                cust = stripe.Customer.update(cust_id, source=token)
                msg = "Customer record updated"
            elif cust_name:
                cust = stripe.Customer.create(name=cust_name, source=token)
                msg = "New customer created"
            else:
                cust, msg = (
                    False,
                    "No customer information provided in request",
                )
        else:
            cust, msg = False, "Stripe token not provided"

        return cust, msg

    @action(detail=False, methods=["post"])
    def ach(self, request):
        amount = request.data.get("amount", 0)
        currency = request.data.get("currency", "usd")
        cust, msg = self.handle_customer(request)
        resp = None
        if cust:
            try:
                account = stripe.Customer.retieve_source(
                    cust.id, cust.default_source
                )
                account.verify(amounts=[32, 40])
                stripe.Charge.create(
                    amount=amount, currency=currency, custoner=cust.id
                )
            except Exception as e:
                resp = Response(data={"msg": str(e)}, status=503)
        else:
            resp = Response(data={"msg": msg}, status=500)
        return resp

    def create(self, request, *args, **kwargs):
        data = dict()
        status = None
        cust, _ = self.handle_customer(request)
        kwargs = {
            "amount": request.data.get("amount", 0),
            "currency": request.data.get("currency", "usd"),
            "description": "Legacy Charge example",
            "source": request.data.get("stripeToken"),
        }
        if cust:
            kwargs["customer"] = cust.id
            _ = kwargs.pop("source")
        try:
            charge = stripe.Charge.create(**kwargs)
            data = {"msg": "Charge created!", "charge_id": charge.id}
            status = 200
        except stripe.error.CardError as e:
            data[
                "msg"
            ] = f"""
                Request status: {e.http_status}\n
                Code: {e.code}\n
                Param: {e.param}\n
                Message: {e.user_message}
            """
            status = 503
        except Exception as e:
            data["msg"] = str(e)
            status = 500
        return Response(data=data, status=status)


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = models.Invoice.objects.all()
    serializer_class = serializers.InvoiceSerializer


class SetupIntentViewSet(viewsets.ModelViewSet, RequestKwargs):
    queryset = models.SetupIntent.objects.all()
    serializer_class = serializers.SetupIntentSerializer
    API_KWARGS = [
        "payment_method_types",
        "customer",
        "payment_method_options",
        "confirm",
        "description",
        "metadata",
        "payment_method",
        "usage",
        "attach_to_self",
        "automatic_payment_methods",
        "flow_directions",
        "mandate_data",
        "on_behalf_of",
        "payment_method_data",
        "return_url",
        "single_use",
    ]

    def create(self, request, *args, **kwargs):

        client = self.get_client(request)
        si_kwargs = self.get_kwargs(request)
        data, status = dict(), None
        try:
            intent = client.setup_intents.create(si_kwargs)
            data, status = {
                "client_secret": intent.client_secret,
                "id": intent.id,
                "intent": intent,
            }, 200
        except Exception as e:
            data["msg"] = str(e)
            status = 500
        return Response(data=data, status=status)


class SubscriptionViewSet(viewsets.ModelViewSet, RequestKwargs):
    queryset = models.Subscription.objects.all()
    serializer_class = serializers.SubscriptionSerializer
    API_KWARGS = [
        "customer",
        "payment_behavior",
        "items",
        "metadata",
        "add_invoice_items",
        "cancel_at_period_end",
        "currency",
        "default_payment_method",
        "description",
        "application_fee_percent",
        "automatic_tax",
        "backdate_start_date",
        "billing_cycle_anchor",
        "billing_threshold",
        "cancel_at",
        "collection_method",
        "coupon",
        "days_until_due",
        "default_source",
        "default_tax_rates",
        "off_session",
        "on_behalf_of",
        "payment_settings",
        "pending_invoice_item_interval",
        "promotion_code",
        "transfer_data",
        "trial_end",
        "trial_from_plan",
        "trial_period_days",
    ]

    def get_queryset(self):
        qs = super().get_queryset()
        customer_id = self.request.query_params.get("customer_id", False)
        if customer_id:
            qs.filter(data__customer=customer_id)
        return qs

    def create(self, request, *args, **kwargs):
        sub_kwargs = self.get_kwargs(request)
        sub_kwargs["expand"] = ["latest_invoice.payment_intent"]
        try:
            subscription = stripe.Subscription.create(**sub_kwargs)
            resp = Response(data={"subscription": subscription}, status=200)
        except Exception as e:
            logger.error(str(e))
            resp = Response(data={"msg": str(e)}, status=500)

        return resp

    def update(self, request, *args, **kwargs):
        """
        Allow user to update their subscription, one item at a time

        Args:
            request (HttpRequest): Incoming PUT request

        Returns:
            Response: API JsonResponse
        """
        subscription_id = self.get_object().id
        price_id = request.data.get("price_id", False)
        product_id = request.data.get("product_id", False)
        one_time = request.data.get("one_time", False)
        if all([price_id, product_id]):
            try:
                updated_subscription = stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=one_time,
                    items=[{"id": product_id, "price": price_id}],
                )
                response = Response(
                    data={"updated_subscription": updated_subscription},
                    status=200,
                )
            except Exception as e:
                response = Response(data={"msg": str(e)}, status=503)
        else:
            response = Response(
                data={"msg": "No product or price provided"}, status=400
            )

        return response

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        try:
            deletedSubscription = stripe.Subscription.deleted(pk)
            return Response(data=deletedSubscription, status=202)
        except Exception as e:
            return Response(data={"msg": str(e)}, status=403)

    @action(detail=True, methods=["post"])
    def preview_change(self, request, pk=None):
        customer_id = request.data.get()
        price_id = request.data.get("price_id", False)
        product_id = request.data.get("product_id", False)
        if all([customer_id, price_id, product_id]):
            # TODO: Figure out how to handle this without hardcoding
            pass

    @action(detail=False, methods=["post"])
    def customer_payment(self, request):
        payment_method_id = request.data.get("payment_method_id", False)
        if payment_method_id:
            try:
                payment_method = stripe.PaymentMethod.retrieve(
                    payment_method_id
                )

                response = Response(
                    data={"payment_method": payment_method}, status=200
                )
            except Exception as e:
                response = Response(data={"msg": str(e)}, status=503)
        else:
            response = Response(
                data={"msg": "No payment method ID provided"}, status=400
            )

        return response

    @action(detail=False, methods=["get", "post"])
    def customer_portal(self, request):
        if request.method == "GET":
            # TODO: Build out interface to configure portal session
            pass
        elif request.method == "POST":
            # TODO: Build out portal session creation and return URL
            pass


class ReaderViewSet(viewsets.ModelViewSet, RequestKwargs):

    LOCATION = "tml_EjcYGgOZ8xQ1m3"
    REQUIRED_KWARGS = []
    API_KWARGS = [
        "type",
        "cart",
        "collect_config",
        "process_config",
        "customer_consent_collected",
        "payment_intent",
        "setup_intent",
        "expand",
    ]
    queryset = models.Reader.objects.all()
    serializer_class = serializers.ReaderSerializer

    @action(detail=False, methods=["post"])
    def connection_token(self, request):
        token = stripe.terminal.ConnectionToken.create()
        return Response({"secret": token.secret})
        # return Response({}, status=500)

    @action(methods=["POST"], detail=False)
    def configure_tips(self, request):
        result = {}
        try:
            tip_kwargs = self.get_kwargs(request)
            logger.info(tip_kwargs)
            config = stripe.terminal.Configuration.create(
                tipping={
                    "usd": {
                        "smart_tip_threshold": 1000,
                        "percentages": [15, 20, 25],
                        "fixed_amounts": [100, 200, 300],
                    }
                }
            )
            stripe.terminal.Location.modify(
                self.LOCATION, configuration_overrides=config.id
            )
            result["status"] = "Succeeded"
            result["message"] = "Tipping configured"
        except Exception as e:
            result["status"] = "Failed"
            result["error"] = str(e)

        return Response(result)

    @action(methods=["POST"], detail=True)
    def process_intent(self, request, pk=None):
        kwargs = self.get_kwargs(request)
        logger.info(f"Kwargs received: {kwargs}")
        response = None
        if "setup_intent" in kwargs.keys():
            try:
                stripe.terminal.Reader.process_setup_intent(pk, **kwargs)
                response = Response(
                    data={"msg": "Reader processing setup intent"}, status=200
                )
            except Exception as e:
                response = Response(data={"msg": str(e)}, status=500)
        else:
            try:
                stripe.terminal.Reader.process_payment_intent(pk, **kwargs)
                response = Response(
                    data={"msg": "Reader processing payment intent"},
                    status=200,
                )
            except Exception as e:
                response = Response(data={"msg": str(e)}, status=500)
        return response

    @action(methods=["GET"], detail=True)
    def reader_status(self, request, pk=None):
        status = stripe.terminal.Reader.retrieve(pk)
        return Response(data=status, status=200)

    @action(methods=["POST"], detail=True)
    def show_cart(self, request, pk=None):
        cart_kwargs = self.get_kwargs(request)
        logger.info(cart_kwargs)
        try:
            stripe.terminal.Reader.set_reader_display(
                pk, type="cart", cart=cart_kwargs["cart"]
            )
            return Response(status=200)
        except Exception as ex:
            logger.error(str(ex))
            return Response(data={"message": str(ex)}, status=500)

    @action(methods=["POST"], detail=True)
    def cancel_action(self, request, pk=None):
        try:
            stripe.terminal.Reader.cancel_action(pk)
            return Response(status=200)
        except Exception as ex:
            return Response(data={"message": str(ex)}, status=500)

    @action(methods=["POST"], detail=True)
    def collect_inputs(self, request, pk=None):
        # TODO: Implement this method when Python SDK supports it
        pass

    def list(self, request):
        kwargs = self.get_kwargs(request)
        readers = stripe.terminal.Reader.list(**kwargs)
        return Response(data=readers, status=200)


class IssuingViewSet(viewsets.ViewSet):
    BILLING_ADDRESS = {
        "address": {
            "line1": "123 Main Street",
            "city": "San Francisco",
            "state": "CA",
            "postal_code": "94111",
            "country": "US",
        },
    }

    @action(methods=["POST"], detail=False)
    def topup(self, request):
        date_str = date.today().strftime("%b %d, $Y")
        amount = request.data.get("amount", 4000)
        currency = request.data.get("currency", "usd")
        result = {}
        try:
            stripe.Topup.create(
                destination_balance="issuing",
                amount=amount,
                currency=currency,
                description=f"Top-up for issuing on {date_str}",
                statement_description="TOP-UP",
            )
            result["status"] = "Success"
            result["message"] = f"Issuing balance topup for {amount} created"
        except Exception as e:
            result["status"] = "Failure"
            result["error"] = str(e)
        return Response(result)

    @action(method=["POST"], detail=False)
    def cardholder(self, request):
        result = {}
        try:
            card_holder = stripe.issuing.Cardholder.create(
                name=request.data.get("name", "Robert Frog"),
                email=request.data.get("email", "bob@frog.io"),
                phone_nummber=request.data.get("phone_number", "+18888675309"),
                status=request.data.get("status", "active"),
                type=request.data.get("type", "individual"),
                billing=self.BILLING_ADDRESS,
            )
            result["status"] = "Success"
            result["cardholder_id"] = card_holder.id
        except Exception as e:
            result["status"] = "Failure"
            result["error"] = str(e)
        return Response(result)

    @action(methods=["POST"], detail=False)
    def card(self, request):
        result = {}
        cardholder_id = request.data.get("cardholder_id", False)
        if not cardholder_id:
            return Response(
                {"error": "Invalid request. Cardholder ID required"},
                status=400,
            )
        try:
            card = stripe.issuing.Card.create(
                carholder=cardholder_id,
                currency=request.data.get("currency", "usd"),
                type=request.data.get("card_type", "virtual"),
            )
            result["status"] = "Success"
            result["card_id"] = card.id
        except Exception as e:
            result["status"] = "Failure"
            result["error"] = str(e)

        return Response(result)

    @action(method=["POST"], detail=False)
    def activate_card(self, request):
        result = {}
        card_id = request.data.get("card_id", False)
        if not card_id:
            return Response(
                {"error": "Invalid request. Card ID required"}, status=400
            )
        try:
            stripe.issuing.Card.modify(card_id, status="active")
            result["status"] = "Success"
            result["message"] = "Card activated"
        except Exception as e:
            result["status"] = "Failed"
            result["error"] = str(e)

        return Response(result)

    @action(method=["GET"], detail=False)
    def create_payment_method(self, request):
        result = {}
        card_id = request.data.get("card_id", False)
        expand = request.data.get("expand", ["number", "cvc"])
        if not card_id:
            return Response(
                {"error": "Invalid request. Card ID required"}, status=400
            )
        try:
            card = stripe.issuing.Card.retrieve(card_id, expand=expand)
            pm = stripe.PaymentMethod.create(
                type="card",
                card={
                    "number": card.number,
                    "exp_month": card.exp_month,
                    "exp_year": card.exp_year,
                },
            )
            result["status"] = "Success"
            result["payment_method_id"] = pm.id
        except Exception as e:
            result["status"] = "Failure"
            result["error"] = str(e)

        return Response(result)


class OrdersViewSet(viewsets.ModelViewSet, RequestKwargs):
    """
    Viewset providing API methods for Orders objects
    """

    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

    REQUIRED_KWARGS = ["currency", "line_items"]
    API_KWARGS = REQUIRED_KWARGS + [
        "customer",
        "description",
        "metadata",
        "payment",
        "automatic_tax",
        "billing_details",
        "discounts",
        "ip_address",
        "shipping_cost",
        "shipping_details",
        "tax_details",
    ]

    def create(self, request, *args, **kwargs):
        stripe.api_version = "2020-08-27; orders_beta=v4"
        order_kwargs = self.get_kwargs(request)
        order_kwargs["expand"] = ["line_items"]
        logger.info(order_kwargs)
        try:
            order = stripe.Order.create(**order_kwargs)
            # models.Order.objects.create(id=order.id, data=order)
        except Exception as e:
            raise e

        return Response(
            data={"client_secret": order.client_secret, "order_id": order.id},
            status=200,
        )

    def list(self, request, *args, **kwargs):
        qs = self.queryset
        if request.query_params.get("customer", False):
            qs = qs.filter(data__customer=request.query_params["customer"])
        if request.query_params.get("status", False):
            qs = qs.filter(data__status=request.query_params["status"])

        qs = self.paginate_queryset(qs)
        serializer = self.serializer_class(qs, many=True)
        return self.get_paginated_response(data=serializer.data)

    @action(methods=["POST"], detail=True)
    def sync(self, request, pk=None):
        stripe.api_version = "2020-08-27; orders_beta=v4"
        order = self.get_object()
        try:
            stripeOrder = stripe.Order.retrieve(
                order.id, expand=["line_items.data.product"]
            )
            self.queryset.filter(id=order.id).update(data=stripeOrder)
        except Exception as e:
            raise e

        return Response(
            data={
                "message": "Record sync successful",
                "order": stripeOrder,
                "success": True,
            },
            status=200,
        )


class AccountViewSet(viewsets.ModelViewSet):
    queryset = models.StripeAccount.objects.all()
    serializer_class = serializers.AccountSerializer


class AppAccountViewSet(viewsets.ModelViewSet):
    queryset = models.AppAccount.objects.all()
    serializer_class = serializers.AppAccountSerializer
    DAYS_BACK = 7

    def list(self, request, *args, **kwargs):
        response_data = [
            {"id": "acct_1Kr3CJRSxigF24b2"},
            {"id": "acct_1K9GySRNhW8G2yaj"},
            {"id": "acct_1JtyGXRBbXxep8eb"},
        ]
        return Response(data=response_data, status=200)

    @action(detail=True, methods=["GET", "POST"])
    def payments(self, request, pk=None):
        days_back = (
            self.DAYS_BACK
            if not request.data.get("days_back")
            else request.data.get("days_back")
        )
        timestamp = round(
            (datetime.now() - timedelta(days=days_back)).timestamp()
        )
        created_dict = {"gt": timestamp}

        charges = stripe.Charge.list(
            limit=100, created=created_dict, stripe_account=pk
        )
        resp_data = [
            {
                "id": ch.id,
                "created": datetime.utcfromtimestamp(ch.created).strftime(
                    "%m/%d/%y"
                ),
                "amount": ch.amount_captured,
            }
            for ch in charges
        ]

        return Response(data=resp_data, status=200)


class TestClockViewSet(viewsets.ModelViewSet, RequestKwargs):
    queryset = models.TestClock.objects.all()
    serializer_class = serializers.TestClockSerializer

    REQUIRED_KWARGS = ["frozen_time"]
    API_KWARGS = ["frozen_time", "name"]

    def create(self, request):
        kwargs = self.get_kwargs(request)
        test_clock = stripe.test_helpers.TestClock.create(**kwargs)
        return Response(data={"test_clock": test_clock}, status=200)

    @action(detail=True, methods=["post"])
    def advance(self, request, pk=None):
        kwargs = self.get_kwargs(request)
        test_clock = stripe.test_helpers.TestClock.advance(pk, **kwargs)
        return Response(
            data={"test_clock": json.dumps(test_clock)}, status=200
        )


class PaymentLinkViewSet(viewsets.ViewSet):
    """Viewset for creating, listing Payment Links through the API"""

    REQUIRED_KWARGS = []
    API_KWARGS = []


class PromoCodeViewSet(viewsets.ViewSet):
    """API viewset for reading promno codes"""

    def list(self, request):
        promo_codes = stripe.PromotionCode.list()
        return Response(data={"promo_codes": promo_codes["data"]}, status=200)

    def retrieve(self, request, pk=None):
        promo_code = stripe.PromotionCode.retrieve(pk)
        return Response(data={"promo_code": promo_code}, status=200)


class ConnectionTokenViewSet(viewsets.ViewSet):
    """API viewset for creating connection tokens"""

    def create(self, request):
        ct = stripe.terminals.ConnectionToken.create()
        return Response(data={"connection_token": ct}, status=200)


class TaxRateViewSet(viewsets.ModelViewSet):
    queryset = models.TaxRate.objects.all()
    serializer_class = serializers.TaxRateSerializer


class TaxCalculationViewSet(viewsets.ViewSet, RequestKwargs):
    REQUIRED_KWARGS = [
        "currency",
        "line_items",
    ]
    API_KWARGS = REQUIRED_KWARGS + [
        "shipping_cost",
        "ship_from_details",
        "tax_date",
        "customer_details",
        "customer",
    ]

    def create(self, request):
        kwargs = self.get_kwargs(request)
        try:
            tax_calc = stripe.tax.Calculation.create(**kwargs)
            return Response(data={"tax_calculation": tax_calc}, status=200)
        except Exception as e:
            return Response(data={"error": str(e)}, status=500)

    @action(detail=True, methods=["post"])
    def create_transaction(self, request, pk=None):
        reference = request.data.get("reference")
        if not reference:
            return Response(
                data={
                    "error": {
                        "code": "Invalid request",
                        "message": "Reference required",
                    }
                },
                status=400,
            )
        try:
            transaction = stripe.tax.Transaction.create_from_calculation(
                calculation=pk, reference=reference, expand=["line_items"]
            )
            return Response(data={"transaction": transaction}, status=200)
        except Exception as e:
            return Response(data={"error": str(e)}, status=500)


class ConnectAccountViewSet(viewsets.ModelViewSet, RequestKwargs):

    API_KWARGS = [
        "email",
        "capabilities",
        "business_type",
        "company",
        "individual",
        "metadata",
        "tos_acceptance",
        "account_token",
        "business_profile",
        "default_currency",
        "documents",
        "external_account",
        "settings",
        "type",
        "country",
        "controller",
    ]
    queryset = models.Account.objects.all()
    serializer_class = serializers.ConnectSerializer
    basename = "connect-account"

    def get(self, request, *args, **kwargs):
        accounts = stripe.Account.list(limit=20)
        return Response(data={"accounts": accounts}, status=200)

    def create(self, request, *args, **kwargs):
        kwargs = self.get_kwargs(request)
        account = stripe.Account.create(**kwargs)
        # Normally I handle this with webhooks but Connected Account events are weird
        models.Account.objects.create(id=account.id, data=account)
        return Response(data={"account": account}, status=200)

    @action(detail=True, methods=["post"])
    def onboarding_link(self, request, pk=None):
        account = self.get_object()
        account_link = stripe.AccountLink.create(
            account=account.id,
            refresh_url=request.data.get("refresh_url"),
            return_url=request.data.get("return_url"),
            type="account_onboarding",
        )
        return Response(data={"account_link": account_link}, status=200)

    @action(detail=True, methods=["post"])
    def set_external_account(self, request, pk=None):
        account = self.get_object()
        token = stripe.Token.create(
            stripe_account=account.id,
            bank_account={
                "payment_method": request.data.get("payment_method")
            },
            customer=request.data.get("customer"),
        )
        stripe.Account.modify(
            "acct_1JticYIlCeH6bP8R",
            stripe_account=account.id,
            external_account=token.id,
        )

        return Response(data={"account": account}, status=200)

    @action(detail=True, methods=["post"])
    def account_session(self, request, pk=None):
        # Defining component types we can use
        components = {
            "account_management": {
                "enabled": True,
                "features": {
                    "external_account_collection": True,
                },
            },
            "account_onboarding": {
                "enabled": True,
                "features": {
                    "external_account_collection": True,
                },
            },
            "balances": {
                "enabled": True,
                "features": {
                    "edit_payout_schedule": True,
                    "instant_payouts": True,
                    "standard_payouts": True,
                },
            },
            "documents": {
                "enabled": True,
            },
            "notification_banner": {
                "enabled": True,
                "features": {
                    "external_account_collection": True,
                },
            },
            "payment_details": {
                "enabled": True,
                "features": {
                    "capture_payments": True,
                    "destination_on_behalf_of_charge_management": True,
                    "dispute_management": True,
                    "refund_management": True,
                },
            },
            "payments": {
                "enabled": True,
                "features": {
                    "capture_payments": True,
                    "destination_on_behalf_of_charge_management": True,
                    "dispute_management": True,
                    "refund_management": True,
                },
            },
            "payouts": {
                "enabled": True,
                "features": {
                    "edit_payout_schedule": True,
                    "instant_payouts": True,
                    "standard_payouts": True,
                },
            },
            "payouts_list": {"enabled": True},
        }

        try:
            key = request.data.get("component")
            if key:
                key = key.replace("-", "_")
                components = {key: components[key]}
            account_session = stripe.AccountSession.create(
                account=pk, components=components
            )
            response = Response(
                data={"client_secret": account_session.client_secret},
                status=200,
            )
        except Exception as e:
            response = Response(data={"msg": str(e)}, status=500)

        return response


class DomainViewSet(viewsets.ModelViewSet, RequestKwargs):
    queryset = models.PaymentMethodDomain.objects.all()
    serializer_class = serializers.DomainSerializer

    REQUIRED_KWARGS = ["domain_name"]
    API_KWARGS = REQUIRED_KWARGS + [
        "enabled",
    ]

    def create(self, request, *args, **kwargs):
        kwargs = self.get_kwargs(request)
        domain = stripe.PaymentMethodDomain.create(**kwargs)
        return Response(data={"domain": domain}, status=200)

    def list(self, request):
        domains = stripe.PaymentMethodDomain.list()
        return Response(data={"domains": domains}, status=200)


class PublishableKey(viewsets.ViewSet):
    """Viewset for retrieving publishable key"""

    def list(self, request):
        pk = stripe.api_key
        return Response(data={"publishable_key": pk}, status=200)


class ConfirmationTokenViewSet(viewsets.ViewSet):
    """Viewset for creating confirmation tokens"""

    def create(self, request):
        token = stripe.ConfirmationToken.create(
            account=request.data.get("account"),
            type=request.data.get("type"),
            redirect_url=request.data.get("redirect_url"),
        )
        return Response(data={"confirmation_token": token}, status=200)

    @action(detail=True, methods=["post"])
    def summary(self, request, pk=None):
        token = stripe.ConfirmationToken.retrieve(pk)
        return Response(data={"confirmation_token": token}, status=200)


class BillingMeterViewSet(viewsets.ViewSet, RequestKwargs):
    REQUIRED_KWARGS = ["default_aggregation", "display_name", "event_name"]
    API_KWARGS = REQUIRED_KWARGS + [
        "customer_mapping",
        "event_time_window",
        "walue_settings",
    ]

    def list(self, request):
        meters = stripe.billing.Meter.list()
        return Response(data={"meters": meters}, status=200)

    def create(self, request):
        kwargs = self.get_kwargs(request)

        meter = stripe.billing.Meter.create(**kwargs)
        return Response(data={"meter": meter}, status=200)

    @action(detail=True, methods=["post"])
    def create_event(self, request, pk=None):
        meter = stripe.billing.Meter.retrieve(pk)

        event = stripe.billing.Meter.create_event(
            event_name=meter.event_name,
            payload={
                "value": request.data.get("value"),
                "stripe_customer_id": request.data.get("customer_id"),
            },
        )
        return Response(data={"event": event}, status=200)

    @action(detail=True, methods=["post"])
    def report_usage(self, request, pk=None):
        usage = stripe.billing.Meter.list_event_summaries(
            pk,
            customer=request.data.get("customer_id"),
            start_time=request.data.get("start_time"),
            end_time=request.data.get("end_time"),
        )
        return Response(data={"usage": usage}, status=200)
