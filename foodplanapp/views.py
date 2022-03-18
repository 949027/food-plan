from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import OrderForm
from .models import Price


@login_required
def order(request):
    total_price = 0
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            price = Price.objects.first()
            order.user = request.user
            if order.menu_type == 'classic':
                start_price = order.duration * price.classic_menu
            elif order.menu_type == 'low_calorie':
                start_price = order.duration * price.low_calorie_menu
            elif order.menu_type == 'vegan':
                start_price = order.duration * price.vegan_menu
            elif order.menu_type == 'keto':
                start_price = order.duration * price.keto_menu
            total_price = start_price + (order.breakfast * price.meal) \
                          + (order.lunch * price.meal) \
                          + (order.dinner * price.meal) \
                          + (order.dessert * price.meal) \
                          + (order.new_year_menu * price.new_year_menu) \
                          + (order.allergy1 * price.allergy) \
                          + (order.allergy2 * price.allergy) \
                          + (order.allergy3 * price.allergy)
            order.total_price = total_price
            order.save()
        return render(request, 'order.html', {
            'form': form,
            'total_price': total_price,
            'order_id': order.id,
        })
    form = OrderForm()
    return render(request, 'order.html', {
        'form': form,
        'total_price': total_price,
    })
