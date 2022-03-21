from django.db import models

from foodplanapp.models import Order


class OrderPayment(models.Model):
    payment_id = models.SlugField(
        "ID платежа в Юкасса",
        max_length=100,
        unique=True
    )
    order = models.OneToOneField(
        Order,
        verbose_name="Заказ к оплате",
        related_name="payment",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField("Дата создания")
    description = models.CharField("Назначение платежа", max_length=100)
    status = models.CharField("Статус платежа", max_length=30)
    is_test = models.BooleanField("Тестовый платеж?")
    payment_amount = models.IntegerField("Сумма платежа")
    payment_currency = models.CharField("Валюта платежа", max_length=10)
    is_paid = models.BooleanField("Оплачен?")

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Оплата заказа {self.order.id} от {self.created_at}"


class OrderPaymentSummary(OrderPayment):
    class Meta:
        proxy = True
        verbose_name = 'Отчёт по платежам'
        verbose_name_plural = 'Отчеты по платежам'
