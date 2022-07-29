from django.urls import path
from .views import (FarmDetailView, TopFarmersView, DashboardAPIView,
                    NumberOfSalesAPIView, NumberOfFarmViewsAPIView)

urlpatterns = [
    path("", FarmDetailView.as_view()),
    path("top", TopFarmersView.as_view()),
    path("dashboard", DashboardAPIView.as_view()),
    path("sales", NumberOfSalesAPIView.as_view()),
    path("views", NumberOfFarmViewsAPIView.as_view())
]
