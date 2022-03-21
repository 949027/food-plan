from django.contrib.auth.models import User
from django.db import models

ORDER_DURATION = [(3, "3 мес"), (12, "12 мес")]
MENU_TYPE = [
    ("classic", "Классическое меню"),
    ("low_calorie", "Низкокалорийное меню"),
    ("vegan", "Вегетарианское меню"),
    ("keto", "Кето меню"),
]


class Price(models.Model):
    classic_menu = models.IntegerField("Классическое меню, руб/мес")
    low_calorie_menu = models.IntegerField("Низкокалорийное меню, руб/мес")
    vegan_menu = models.IntegerField("Вегетарианское меню, руб/мес")
    keto_menu = models.IntegerField("Кето меню, руб/мес")
    meal = models.IntegerField("Доплата за каждый прием пищи, руб")
    new_year_menu = models.IntegerField("Доплата за новогоднее меню, руб")
    allergy = models.IntegerField("Доплата за гипоаллергенное меню, руб")

    class Meta:
        verbose_name = "цена"
        verbose_name_plural = "цены"


class Order(models.Model):
    menu_type = models.CharField(
        "Тип меню", choices=MENU_TYPE, max_length=100, default="classic"
    )
    duration = models.IntegerField(
        "Срок подписки, мес", choices=ORDER_DURATION
    )
    breakfast = models.BooleanField("Завтраки")
    lunch = models.BooleanField("Обеды")
    dinner = models.BooleanField("Ужины")
    dessert = models.BooleanField("Десерты")
    new_year_menu = models.BooleanField("Новогоднее меню")
    persons_amount = models.IntegerField("Количество персон")
    allergies = models.ManyToManyField(
        "Allergies",
        related_name="orders",
    )
    promo_code = models.CharField(
        "Промокод",
        null=True,
        blank=True,
        max_length=20,
    )
    total_price = models.IntegerField("Стоимость подписки", null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ №{self.id} для {self.user}"


class Allergies(models.Model):
    name = models.CharField(
        "Название",
        max_length=100,
    )
    description = models.TextField(
        "Описание",
        blank=True,
    )

    class Meta:
        verbose_name = "аллергия"
        verbose_name_plural = "аллергии"

    def __str__(self):
        return f"Аллергия на {self.name}"


class Dish(models.Model):
    name = models.CharField(
        "Название",
        max_length=200,
    )
    image = models.ImageField(
        "Изображение",
        upload_to="images/",
        null=True,
    )
    calories = models.FloatField(
        "Калорийность, ккал",
        blank=True,
        null=True,
    )
    weight = models.IntegerField(
        "Вес, г",
        blank=True,
        null=True,
    )
    guide = models.TextField(
        "Инструкция",
        blank=True,
    )
    active = models.BooleanField(
        "Активный",
        default=True,
    )
    menu_type = models.CharField(
        "Тип меню",
        choices=MENU_TYPE,
        max_length=100,
        default="classic",
        db_index=True,
    )
    allergies = models.ManyToManyField(
        "Allergies",
        related_name="dishes",
        blank=True,
    )

    class Meta:
        verbose_name = "рецепт"
        verbose_name_plural = "рецепты"

    def __str__(self):
        return self.name


class Dishitems(models.Model):
    dish = models.ForeignKey(
        "Dish",
        related_name="dishitems",
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )
    ingredient = models.CharField(
        "Наименование",
        max_length=200,
    )
    amount = models.CharField(
        "Количество",
        max_length=10,
        blank=True,
    )
    measurement_unit = models.CharField(
        "Единица измерения",
        max_length=10,
        blank=True,
    )

    class Meta:
        verbose_name = "ингредиент"
        verbose_name_plural = "ингредиенты"

    def __str__(self):
        return self.ingredient


class Promocode(models.Model):
    code = models.CharField("Код", max_length=20, unique=True)
    valid_from = models.DateField("Действует с")
    valid_to = models.DateField("Действует до")
    discount = models.IntegerField("Размер скидки, руб")

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"

    def __str__(self):
        return self.code
