from django.contrib import admin

from .models import User, Order, Dish, Price, Dishitems


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    pass


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    pass


@admin.register(Dishitems)
class DishitemsAdmin(admin.ModelAdmin):
    pass
