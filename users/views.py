from typing import Any
from django.http import HttpRequest
from django.shortcuts import HttpResponseRedirect
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView


from users.models import User, EmailVerification
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket
from common.views import TitleMixin


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy("users:login")
    success_message = 'Вы успешно зарегистрированы!'
    title = 'Store - Регистрация'


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = "Store - Личный кабинет"

    def get_success_url(self) -> str:
        return reverse_lazy('users:profile', args=self.object)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("index"))


class EmailVerificationView(TitleMixin, TemplateView):
    title = "Store - Подтверждение электронной почты"
    template_name = 'users/email_verification.html'

    def get(self, request: HttpRequest, *args: Any,
            **kwargs: Any) -> HttpResponse:
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user,
                                                               code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
