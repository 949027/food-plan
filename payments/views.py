from django.shortcuts import redirect
from django.urls import reverse
from yookassa import Configuration, Payment
from django.conf import settings
import uuid
from urllib.parse import urljoin

from .models import OrderPayment

from foodplanapp.models import Order


def payment(request, order_id):
    Configuration.account_id = settings.SHOP_ID
    Configuration.secret_key = settings.SHOP_TOKEN
    order = Order.objects.get(id=order_id)
    
    return_url = urljoin(
        request.build_absolute_uri(),
        reverse(complete_payment, kwargs={"order_id": order_id})
    )

    payment = Payment.create({
        "amount": {
            "value": order.total_price,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": return_url,
        },
        "capture": True,
        "description": f"Заказ №{order_id}",
        "metadata": {"order_id": order_id},
    }, uuid.uuid4())

    OrderPayment.objects.create(
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
    order_payment = Order.objects.get(id=order_id).payments.first()
    
    Configuration.account_id = settings.SHOP_ID
    Configuration.secret_key = settings.SHOP_TOKEN
    payment = Payment.find_one(order_payment.payment_id)
    
    order_payment.status = payment.status
    order_payment.is_paid = payment.paid
    order_payment.save()
    return redirect(reverse("profile"))
