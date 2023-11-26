from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse

from .forms import RegistrationForm
from django.views.generic import CreateView, DeleteView
from .models import BlogUser
from rest_framework.authtoken.models import Token


# Create your views here.
class UserLoginView(LoginView):
    template_name = 'userapp/login.html'


class UserCreateView(CreateView):
    model = BlogUser
    template_name = 'userapp/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('users:login')

class UserDetailView(DeleteView):
    template_name = 'userapp/profile.html'
    model = BlogUser

def update_token(requst):
    user = requst.user
    try:
        user.auth_token
    except ObjectDoesNotExist:
        Token.objects.create(user=user)
    user.auth_token.delete()
    Token.objects.create(user=user)

    return HttpResponseRedirect(reverse('users:profile', kwargs={'pk': user.pk}))
