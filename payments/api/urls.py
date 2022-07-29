from .views import PaymentsListAPIView
from django.urls import path

urlpatterns = [
    path('', PaymentsListAPIView.as_view())
]
