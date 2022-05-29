from django.shortcuts import render
from django.views.generic import TemplateView


class PreSignupView(TemplateView):
    template_name = 'auth/pre-signup.html'


class SignupView(TemplateView):
    template_name = 'auth/signup.html'


class LoginView(TemplateView):
    template_name = "auth/login.html"
