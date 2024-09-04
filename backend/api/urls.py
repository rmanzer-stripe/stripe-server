"""
    api/urls.py

    Define a set of URLs that map to REST API endpoints.
"""

from django.urls import include, path
from rest_framework import routers
from payments import api_views
from payments import supermanzer_api_views as sapi_views
from . import views


# Intantiate Django REST Framework Router
# https://www.django-rest-framework.org/api-guide/routers/
router = routers.DefaultRouter()
router.register(r'disputes', api_views.DisputeViewSet)
router.register(r'payment_intents', api_views.PaymentIntentViewSet)
router.register(r'customers', api_views.CustomerViewSet)
router.register(r'charges', api_views.ChargeViewSet)
router.register(r'setup_intents', api_views.SetupIntentViewSet)
router.register(r'products', api_views.ProductViewSet)
router.register(r'prices', api_views.PriceViewSet)
router.register(r'subscriptions', api_views.SubscriptionViewSet)
router.register(r'terminals', api_views.ReaderViewSet)
router.register(r'issuing', api_views.InvoiceViewSet)
router.register(r'orders', api_views.OrdersViewSet)
router.register(r'accounts', api_views.AccountViewSet)
router.register(r'app_accounts', api_views.AppAccountViewSet)
router.register(r'test_clocks', api_views.TestClockViewSet)
router.register(r'checkout_sessions',
                api_views.CheckoutSessionViewSet, basename="checkout_sessions")
router.register(r'promo_codes', api_views.PromoCodeViewSet,
                basename="promo_codes")
router.register(r'connection_tokens',
                api_views.ConnectionTokenViewSet, basename="connection_tokens")
router.register(r'tax_rates', api_views.TaxRateViewSet)
router.register(r'connect-accounts', api_views.ConnectAccountViewSet)
router.register(r'payment-domains', api_views.DomainViewSet)
router.register(r'publishable-key',
                api_views.PublishableKey, basename="publishable-key")
router.register(r'confirmation-tokens', api_views.ConfirmationTokenViewSet, basename="confirmation-tokens")
# router.register(r'publishable_key', api_views.PublishableKey)
router.register(r'billing_meters', api_views.BillingMeterViewSet, basename="billing_meters")
router.register(r'tax_calculations', api_views.TaxCalculationViewSet, basename="tax_calculations")

# Routing for Supermanzer API views
router.register(r'supermanzer/prices',
                sapi_views.PriceViewSet, basename="prices")
router.register(r'supermanzer/quotes',
                sapi_views.QuoteViewSet, basename="quotes")



urlpatterns = [
    path('', include(router.urls)),
    path('config', views.get_publishable_key),
    path('custom-si', views.get_custom_si),
    path('payment_sheet', views.payment_sheet),
    path('webhook/', views.WebhookView.as_view()),
]
