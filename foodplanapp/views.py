from datetime import date
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import OrderForm
from .models import Price, Dish, Order, Promocode


@login_required
def order(request):
    total_price = 0
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            price = Price.objects.first()
            order.user = request.user

            Order.objects.filter(user=order.user).delete()

            if order.menu_type == "classic":
                start_price = price.classic_menu
            elif order.menu_type == "low_calorie":
                start_price = price.low_calorie_menu
            elif order.menu_type == "vegan":
                start_price = price.vegan_menu
            elif order.menu_type == "keto":
                start_price = price.keto_menu
            order.save()
            form.save_m2m()
            total_price = (
                order.duration * sum([
                    start_price,
                    (order.breakfast * price.meal),
                    (order.lunch * price.meal),
                    (order.dinner * price.meal),
                    (order.dessert * price.meal),
                    (order.allergies.count() * price.allergy),
                ]) - sum([
                    order.new_year_menu * price.new_year_menu,
                ])
            )
            if order.promo_code:
                promo_codes = Promocode.objects.filter(
                    code=order.promo_code.upper())
                if promo_codes.exists():
                    promo_code = promo_codes.first()
                    if promo_code.valid_from <= date.today() <= promo_code.valid_to:
                        total_price -= promo_code.discount
                    else:
                        order.promo_code = None
                else:
                    order.promo_code = None

            order.total_price = total_price
            order.save()

            return render(
                request,
                "order.html",
                {
                    "form": form,
                    "total_price": total_price,
                    "order_id": order.id,
                    "promo_code": order.promo_code,
                }
            )

    form = OrderForm()
    return render(
        request, "order.html", {"form": form, "total_price": total_price}
    )
