from django.shortcuts import render
from django.views.generic import CreateView

from users.forms import CustomUserCreationForm


class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = 'login'
    template_name = 'registration/register.html'
