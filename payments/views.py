from django.shortcuts import HttpResponse


def payment(request, order_id):
    return HttpResponse(f'Здесь будет страница платежа для заказа {order_id}')
