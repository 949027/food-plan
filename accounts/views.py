from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import forms
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class RegisterationForm(UserCreationForm):
    username = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))    

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUser(auth_views.LoginView):

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, "auth.html", context={
            'form': form
        })

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("profile")


class LogoutUser(auth_views.LogoutView):
    next_page = reverse_lazy('start_page')


class UserCreateView(CreateView):
    form_class = RegisterationForm
    template_name = 'registration.html'

    def __init__(self):
        self.object = None

    def get_success_url(self):
        return reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('profile')


@login_required
def user_profile(request):
    return render(request, 'lk.html', context={'username': request.user.get_username()})
