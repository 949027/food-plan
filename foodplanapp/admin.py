from django.contrib import admin

from .models import Order, Dish, Price


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    pass


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    pass
