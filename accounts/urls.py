from django.urls import path
from .views import DashboardView, SignupView, LoginView, PreSignupView, LogoutView, UserSpecificView


urlpatterns = [
    path('signup', PreSignupView.as_view(), name='pre-signup'),
    path('signup/<str:type>', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('logout', LogoutView.as_view(), name="logout"),
    path('user-view', UserSpecificView.as_view(), name='user-view')
]
