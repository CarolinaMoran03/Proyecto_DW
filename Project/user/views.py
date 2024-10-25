from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from user.forms import CustomUserCreationForm

# Create your views here.


class RegisterUserView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'core/register.html'
    success_url = reverse_lazy('login')
    
    def form_invalid(self, form):
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))