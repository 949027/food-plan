from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import LoginForm, RegistrationForm
from foodplanapp.models import Dish, Order


class LoginUser(auth_views.LoginView):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, "accounts/auth.html", context={"form": form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("profile")


class LogoutUser(auth_views.LogoutView):
    next_page = reverse_lazy("start_page")


class UserCreateView(CreateView):
    form_class = RegistrationForm
    template_name = "accounts/registration.html"

    def __init__(self):
        self.object = None

    def get_success_url(self):
        return reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("profile")


@login_required
def user_profile(request):
    order = (
        Order.objects.prefetch_related("allergies")
        .filter(user__id=request.user.id)
        .first()
    )

    if order:
        allergies = list(
            order.allergies.values(
                "name",
            )
        )

        return render(
            request,
            "accounts/lk.html",
            context={
                "user": request.user,
                "order": order,
                "allergies": allergies,
            },
        )
    else:
        return render(
            request,
            "accounts/lk.html",
            context={
                "user": request.user,
            },
        )


@login_required
def show_receipt(request):
    dish_allergies = []
    dish_items = []

    if request.method == "GET":
        order = Order.objects.prefetch_related("allergies").filter(
            user__id=request.user.id
        )

        allergies = list(order.values_list("allergies", flat=True))

        if allergies != [None]:
            dish = (
                Dish.objects.prefetch_related("allergies")
                .prefetch_related("dishitems")
                .filter(menu_type=order[0].menu_type, active=True)
                .exclude(allergies__in=allergies)
                .order_by("?")
                .first()
            )

            if dish:
                dish_allergies = list(
                    dish.allergies.values(
                        "name",
                    )
                )
        else:
            dish = (
                Dish.objects.filter(menu_type=order[0].menu_type, active=True)
                .prefetch_related("dishitems")
                .order_by("?")
                .first()
            )

        if dish:
            dish_items = list(
                dish.dishitems.values(
                    "ingredient",
                    "amount",
                    "measurement_unit",
                )
            )

        return render(
            request,
            "accounts/receipt.html",
            context={
                "dish": dish,
                "allergies": dish_allergies,
                "dish_items": dish_items,
            },
        )
