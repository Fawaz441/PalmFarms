from django.urls import path
from .views import ConsultantRegisterAPIView

urlpatterns = [
    path("register", ConsultantRegisterAPIView.as_view())
]
