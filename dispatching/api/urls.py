from django.urls import path
from .views import StateListAPIView

urlpatterns = [
    path('states', StateListAPIView.as_view())
]
