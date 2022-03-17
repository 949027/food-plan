from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import forms
from django.contrib.auth.decorators import login_required


# class LoginUserForm(AuthenticationForm):
#     username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

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


class LoginUser(auth_views.LoginView):
    # form_class = LoginUserForm
    # form_class = AuthenticationForm
    # template_name = 'auth.html'
 
    # def get_user_context(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     c_def = self.get_user_context(title="Авторизация")
    #     return dict(list(context.items()) + list(c_def.items()))

    # def get_success_url(self):
    #     return reverse_lazy('profile')
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

        # return render(request, "login.html", context={
        #     'form': form,
        #     'ivalid': True,
        # })


class LogoutUser(auth_views.LogoutView):
    next_page = reverse_lazy('start_page')


@login_required
def user_profile(request):
    return render(request, 'lk.html', context={'username': request.user.get_username()})
