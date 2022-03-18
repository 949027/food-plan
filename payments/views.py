from django.shortcuts import redirect, HttpResponse
from yookassa import Configuration, Payment
from django.conf import settings
import uuid

from .models import OrderPayment

from foodplanapp.models import Order


def payment(request, order_id):
    Configuration.account_id = settings.SHOP_ID
    Configuration.secret_key = settings.SHOP_TOKEN
    order = Order.objects.get(id=order_id)
    payment = Payment.create({
        "amount": {
            "value": order.total_price,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"http://82.148.16.182/payment/complete/{order_id}",
        },
        "capture": True,
        "description": f"Заказ №{order_id}",
        "metadata": {"order_id": order_id},
    }, uuid.uuid4())

    OrderPayment.object.create(
        payment_id=payment.id,
        order=order,
        created_at=payment.created_at,
        description=payment.description,
        status=payment.status,
        is_test=payment.test,
        payment_amount=payment.amount.value,
        payment_currency=payment.amount.currency,
        is_paid=payment.paid,
    )
    return redirect(payment.confirmation.confirmation_url)


def complete_payment(request, order_id):
    order_payment = Order.object.get(order__id=order_id).payments.first()
    payment = Payment.find_one(order_payment.payment_id)
    return HttpResponse(payment)
