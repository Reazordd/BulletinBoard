from django.views.generic import RedirectView
from django.contrib.auth import logout
from django.urls import reverse_lazy
from allauth.account.views import LoginView, SignupView

class CustomLoginView(LoginView):
    template_name = 'account/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

class CustomSignupView(SignupView):
    template_name = 'account/signup.html'

    def get_success_url(self):
        return reverse_lazy('home')

class CustomLogoutView(RedirectView):
    pattern_name = 'home'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)