from django.db.models import Q
from django.shortcuts import render

from .forms import OrderForm
from .models import Price, Dish, Dishitems, Order


def order(request):
    total_price = 0
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            price = Price.objects.first()
            order.user = request.user
            if order.menu_type == "classic":
                start_price = order.duration * price.classic_menu
            elif order.menu_type == "low_calorie":
                start_price = order.duration * price.low_calorie_menu
            elif order.menu_type == "vegan":
                start_price = order.duration * price.vegan_menu
            elif order.menu_type == "keto":
                start_price = order.duration * price.keto_menu
            total_price = (
                start_price
                + (order.breakfast * price.meal)
                + (order.lunch * price.meal)
                + (order.dinner * price.meal)
                + (order.dessert * price.meal)
                + (order.new_year_menu * price.new_year_menu)
                + (order.allergy1 * price.allergy)
                + (order.allergy2 * price.allergy)
                + (order.allergy3 * price.allergy)
            )
            order.total_price = total_price
            order.save()
    else:
        form = OrderForm()
    return render(
        request, "order.html", {"form": form, "total_price": total_price}
    )


def custom_receipt(request):
    order = Order.objects.filter(user__id=1).first()
    filters = {}
    if order.allergy1:
        filters["allergy1"] = order.allergy1
    elif order.allergy2:
        filters["allergy2"] = order.allergy2
    elif order.allergy3:
        filters["allergy3"] = order.allergy3
    if order.allergy1 and order.allergy2:
        filters["allergy1"] = order.allergy1
        filters["allergy2"] = order.allergy2
    if order.allergy1 and order.allergy3:
        filters["allergy1"] = order.allergy1
        filters["allergy3"] = order.allergy3
    if order.allergy2 and order.allergy3:
        filters["allergy2"] = order.allergy2
        filters["allergy3"] = order.allergy3
    if order.allergy1 and order.allergy2 and order.allergy3:
        filters["allergy1"] = order.allergy1
        filters["allergy2"] = order.allergy2
        filters["allergy3"] = order.allergy3

    filter_q = Q(**filters)
    print(filter_q)

    # queryset = Something.objects.exclude(filter_q)

    dish = (
        Dish.objects.filter(menu_type=order.menu_type)
        .exclude(filter_q)
        .order_by("?")
        .first()
    )

    print(dish)

    return render(
        request,
        template_name="lk.html",
        context={
            "dish": dish,
        },
    )
