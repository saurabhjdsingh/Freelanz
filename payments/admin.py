from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import VirtualCurrency, Tempwallet, AccountDetails, Refund, Payment


class VirtualCurrencyAdmin(ModelAdmin):
    list_display = ["user", "budget"]
    search_fields = ["user", "budget"]
    list_filter = ["user", "budget"]


admin.site.register(VirtualCurrency, VirtualCurrencyAdmin)

class RefundAdmin(ModelAdmin):
    list_display = ["user", "budget"]
    search_fields = ["user", "budget"]
    list_filter = ["user", "budget"]


admin.site.register(Refund, RefundAdmin)


class TempwalletAdmin(ModelAdmin):
    list_display = ["user", "budget"]
    search_fields = ["user", "budget"]
    list_filter = ["user", "budget"]


admin.site.register(Tempwallet, TempwalletAdmin)


class AccountDetailscAdmin(ModelAdmin):
    list_display = ["verified", "user", "account_number", "ifsc_code", "account_id", "name"]
    search_fields = ["verified", "user", "account_number", "ifsc_code", "account_id", "name"]
    list_filter = ["verified", "user", "account_number", "ifsc_code", "account_id", "name"]


admin.site.register(AccountDetails, AccountDetailscAdmin)

class PaymentAdmin(ModelAdmin):
    list_display = ["profile", "payment_amount"]
    search_fields = ["profile__user__username", "payment_id", "payment_amount", "email", "phone_number"]
    list_filter = ["payment_amount"]

admin.site.register(Payment, PaymentAdmin)
