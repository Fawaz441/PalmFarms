from django.urls import path
from .views import SignupView, LoginView, PreSignupView


urlpatterns = [
    path('signup', PreSignupView.as_view(), name='pre-signup'),
    path('signup/<str:type>', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login')
]
