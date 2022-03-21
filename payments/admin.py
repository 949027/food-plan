from django.contrib import admin
from django.db.models import DateTimeField
from django.db.models import Count, Sum, Max, Min
from django.db.models.functions import Trunc

from .models import OrderPayment, OrderPaymentSummary
from foodplanapp.models import MENU_TYPE


@admin.register(OrderPayment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'is_paid', 'status', 'created_at',
                    'total_cost', 'order_menu_type', 'payment_id', )
    list_filter = ('is_paid', 'status', 'created_at', 'order__menu_type',)

    def order_menu_type(self, obj):
        return f"{obj.order.get_menu_type_display()}"

    def total_cost(self, obj):
        return f"{obj.payment_amount} {obj.payment_currency}"


def get_next_in_date_hierarchy(request, date_hierarchy):
    if date_hierarchy + '__day' in request.GET:
        return 'hour'
    if date_hierarchy + '__month' in request.GET:
        return 'day'
    if date_hierarchy + '__year' in request.GET:
        return 'month'
    return 'month'


def calc_percents(amount, total):
    if total == 0 or amount == 0:
        return 0
    return amount * 100 / total


@admin.register(OrderPaymentSummary)
class OrderPaymentAdmin(admin.ModelAdmin):
    change_list_template = 'admin/payments_summary_change_list.html'
    date_hierarchy = 'created_at'
    
    list_filter = ('order__menu_type',)
    
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset.filter(is_paid=True)
        except (AttributeError, KeyError):
            return response
        
        metrics = {
            'total': Count('id'),
            'total_sales': Sum('payment_amount'),
        }
        response.context_data['summary'] = list(
            qs
            .values('order__menu_type')
            .annotate(**metrics)
            .order_by('-total_sales')
        )
        
        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )
        #TODO: костыль get_menu_type_display не заработал ???
        menu_types = dict(MENU_TYPE)
        for item in response.context_data["summary"]:
            key = item["order__menu_type"]
            item["order__menu_type"] = menu_types[key]
            item["percent"] = calc_percents(
                item["total_sales"],
                response.context_data['summary_total']["total_sales"]
            ) 

        period = get_next_in_date_hierarchy(request, self.date_hierarchy)
        response.context_data['period'] = period
        summary_over_time = (
            qs
            .annotate(
                period=Trunc('created_at', period, output_field=DateTimeField())
            ).values('period')
            .annotate(total=Sum('payment_amount'))
            .order_by('period')
        )
        summary_range = summary_over_time.aggregate(
            low=Min('total'),
            high=Max('total'),
        )
        high = summary_range.get('high', 0)
        low = summary_range.get('low', 0)
        response.context_data['summary_over_time'] = [{
            'period': x['period'],
            'total': x['total'] or 0,
            'pct': \
               round((x['total'] or 0) / high * 100)
               if high > low else 0,
        } for x in summary_over_time]
        return response

