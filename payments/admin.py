from django.contrib import admin

from .models import OrderPayment


@admin.register(OrderPayment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'is_paid', 'status', 'created_at',
                    'total_cost', 'order_menu_type', 'payment_id', )
    list_filter = ('is_paid', 'status', 'created_at', )

    def order_menu_type(self, obj):
        return f"{obj.order.get_menu_type_display()}"

    def total_cost(self, obj):
        return f"{obj.payment_amount} {obj.payment_currency}"
