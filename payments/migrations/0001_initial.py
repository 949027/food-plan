# Generated by Django 4.0.3 on 2022-03-18 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('foodplanapp', '0008_remove_price_start_price_order_menu_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.SlugField(max_length=100, unique=True, verbose_name='ID платежа в Юкасса')),
                ('created_at', models.DateTimeField(verbose_name='Дата создания')),
                ('description', models.CharField(max_length=100, verbose_name='Назначение платежа')),
                ('status', models.CharField(max_length=30, verbose_name='Статус платежа')),
                ('is_test', models.BooleanField(verbose_name='Тестовый платеж?')),
                ('payment_amount', models.IntegerField(verbose_name='Сумма платежа')),
                ('payment_currency', models.CharField(max_length=10, verbose_name='Валюта платежа')),
                ('is_paid', models.BooleanField(verbose_name='Оплачен?')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='foodplanapp.order', verbose_name='Заказ к оплате')),
            ],
        ),
    ]
