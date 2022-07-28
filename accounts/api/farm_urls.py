from django.urls import path
from .views import FarmDetailView, TopFarmersView

urlpatterns = [
    path("", FarmDetailView.as_view()),
    path("top", TopFarmersView.as_view()),
]
