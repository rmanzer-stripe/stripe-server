from django.contrib import admin
from .models import StripeAccount
# Register your models here.


@admin.register(StripeAccount)
class StripeAccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'account_id', 'country', 'has_connect']

    fieldsets = (
        (None, {
            'fields': ('name', 'account_id', 'country', 'has_connect')
        }),
        ('Test Mode', {
            'fields': ('Test Private Key', 'Test Public Key')
        }),
        ('Live Mode', {
            'fields': ('Live Private Key', 'Live Public Key')
        })
    )
