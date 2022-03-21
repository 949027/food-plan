from django import forms

from .models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = (
            'menu_type',
            'duration',
            'breakfast',
            'lunch',
            'dessert',
            'dinner',
            'new_year_menu',
            'persons_amount',
            'allergy1',
            'allergy2',
            'allergy3',
            'promo_code',
        )


