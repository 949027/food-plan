from django.contrib import admin

from .models import OrderPayment


@admin.register(OrderPayment)
class PaymentAdmin(admin.ModelAdmin):
    pass

