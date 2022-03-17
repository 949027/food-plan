from django.contrib.auth.models import User
from django.db import models

ORDER_DURATION = [(3, '3 мес'), (12, '12 мес')]


class Price(models.Model):
    start_price = models.IntegerField('Месяц подписки, руб')
    meal = models.IntegerField('Доплата за каждый прием пищи, %')
    new_year_menu = models.IntegerField('Доплата за новогоднее меню, %')
    allergy = models.IntegerField('Доплата за гипоаллергенное меню, %')
    promo_code = models.IntegerField('Скидка за промокод, %')


class Order(models.Model):
    duration = models.IntegerField(
        'Срок подписки, мес',
        choices=ORDER_DURATION
    )
    breakfast = models.BooleanField('Завтраки')
    lunch = models.BooleanField('Обеды')
    dinner = models.BooleanField('Ужины')
    dessert = models.BooleanField('Десерты')
    new_year_menu = models.BooleanField('Новогоднее меню')
    persons_amount = models.IntegerField('Количество персон')
    allergy1 = models.BooleanField('Аллергия 1')
    allergy2 = models.BooleanField('Аллергия 2')
    allergy3 = models.BooleanField('Аллергия 3')
    promo_code = models.CharField(
        'Промокод',
        max_length=20,
        blank=True,
        null=True
    )
    total_price = models.IntegerField('Стоимость подписки')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    def __str__(self):
        return f'Заказ №{self.id}'


class Dish(models.Model):
    name = models.CharField('Название', max_length=200)
    ingredients = models.TextField('Ингридиенты')
    image = models.ImageField('Изображение')
    calories = models.IntegerField('Калорийность, ккал')
    weight = models.IntegerField('Вес, г')

    def __str__(self):
        return self.name
