from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from yookassa import Configuration, Payment
from django.conf import settings
import uuid


def payment(request, order_id):
    Configuration.account_id = settings.SHOP_ID
    Configuration.secret_key = settings.SHOP_TOKEN
    payment = Payment.create({
        "amount": {
            "value": "100.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "http://82.148.16.182/payment/complete/",
        },
        "capture": True,
        "description": f"Заказ №{order_id}",
        "metadata": {"order_id": order_id},
    }, uuid.uuid4())
    return redirect(payment.confirmation.confirmation_url)


def complete_payment(request):
    return HttpResponse(request)
