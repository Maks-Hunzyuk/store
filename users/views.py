from typing import Any
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView


from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket
from common.views import TitleMixin


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user=user)
                return HttpResponseRedirect(reverse("index"))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, template_name="users/login.html", context=context)


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy("users:login")
    success_message = 'Вы успешно зарегестрированы!'
    title = 'Store - Регистрация'


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = "Store - Личный кабинет"

    def get_success_url(self) -> str:
        return reverse_lazy('users:profile', args=(self.object))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context  = super(UserProfileView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("index"))
