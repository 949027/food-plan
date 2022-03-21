from django import forms

from .models import Order, Allergies


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
            'allergies',
            'promo_code',
        )

    allergies = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Allergies.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
