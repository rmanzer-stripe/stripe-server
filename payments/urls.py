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

    # FBVs
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('webhook/', views.stripe_webhook),
    path('webhook2/', views.webhook2),
    path('.well-known/apple-developer-merchantid-domain-association',
         views.host_apple_stuff)
]
