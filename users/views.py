from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import CustomUserCreationForm


class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Registration failed. Please correct the errors.')
        return super().form_invalid(form)