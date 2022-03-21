from django.contrib import admin

from .models import Order, Dish, Price, Dishitems, Promocode,  Allergies


class DishitemsInline(admin.TabularInline):
    model = Dishitems
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    pass


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    inlines = [DishitemsInline]


@admin.register(Dishitems)
class DishitemsAdmin(admin.ModelAdmin):
    pass
