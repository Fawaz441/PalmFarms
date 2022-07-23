from django.urls import path
from .views import ConsultantRegisterAPIView, ConsultingRequestAPIView

urlpatterns = [
    path("register", ConsultantRegisterAPIView.as_view()),
    path("request", ConsultingRequestAPIView.as_view())
]
