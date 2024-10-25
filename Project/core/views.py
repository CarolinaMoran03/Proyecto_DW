from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import *
# Create your views here.



class CoreLoginView(LoginView):
    template_name = 'core/login.html'
    next_page = 'job'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('job')
            
        return super().dispatch(request, *args, **kwargs)

        


class RegisterView(TemplateView):
    template_name = 'core/register.html'

class CoreLogoutView(LogoutView):
    next_page = "login"




