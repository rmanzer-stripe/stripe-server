# payments/urls.py

from django.urls import path

from . import views

app_name = 'payments'
urlpatterns = [
    # CBVs
    path('', views.HomePageView.as_view(), name='home'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancelled/', views.CancelledView.as_view(), name='cancelled'),
    path('disputes/', views.DisputeList.as_view(), name="dispute-list"),
    path('disputes/<str:id>/evidence/',
         views.ProvideEvidence.as_view(), name='provide-evidence'),
    path('pi_checkout/', views.PaymentIntent.as_view(), name='payment-intent'),
    path('pi-hold/', views.PaymentIntentHold.as_view(), name='pi-hold'),
    path('capture/', views.CapturePayments.as_view(), name='capture'),
    path('payment-upe', views.UPE.as_view(), name='payment-upe'),
    path('request-btn', views.RequestBtn.as_view(), name='request-btn'),
    path('payment-refund', views.PaymentIntentRefund.as_view(),
         name='payment-refund'),
    path('legacy-payment', views.LegacyElementPage.as_view(),
         name='legacy-payment'),
    path('ach', views.ACHCharge.as_view(), name='ach'),
    path('setup-intent', views.SetupIntent.as_view(), name='setup-intent'),
    path('subscribe', views.SubscriptionView.as_view(), name='subscribe'),
    path('manage-billing', views.ManageSubscriptions.as_view(), name='manage-sub'),
    path('checkout-link', views.CheckoutLink.as_view(), name='checkout-link'),
    path('invoices', views.InvoiceView.as_view(), name='invoices'),
    path('checkout-subscribe', views.CheckoutView.as_view(),
         name='checkout-subscribe'),
    path('payment-info', views.SubPaymentInfo.as_view(), name='payment-info'),
    path('old-subscription', views.OldSubscriptionView.as_view(),
         name='old-subscription'),
    path('create-customer', views.OldSubscriptionView.as_view(),
         name='create-customer'),
    path('create-subscription', views.OldSubscriptionView.as_view(),
         name='create-subscription'),
    path('retry-invoice', views.OldSubscriptionView.as_view(), name='retry-invoice'),
    path('customer-portal', views.CustomerPortalView.as_view(),
         name='customer-portal'),
    path('connect-accounts', views.ConnectAccountsView.as_view(),
         name="connect-accounts"),
    path('connect-sale', views.ConnectAccountsView.as_view(),
         name="connect-sale"),
    path('add-connect-customer', views.ConnectAccountsView.as_view(),
         name='add-connect-customer'),
    path('make-transfers', views.ConnectAccountsView.as_view(),
         name='make-transfers'),
    # FBVs
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('webhook/', views.stripe_webhook),
    path('webhook2/', views.webhook2),
    path('.well-known/apple-developer-merchantid-domain-association',
         views.host_apple_stuff)
]
