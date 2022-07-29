from django.urls import path
from .views import (FarmListView, FarmDetailView, TopFarmersView, DashboardAPIView,
                    NumberOfSalesAPIView, NumberOfFarmViewsAPIView)

urlpatterns = [
    path("", FarmListView.as_view()),
    path("visit_farm", FarmDetailView.as_view()),
    path("top", TopFarmersView.as_view()),
    path("dashboard", DashboardAPIView.as_view()),
    path("sales", NumberOfSalesAPIView.as_view()),
    path("views", NumberOfFarmViewsAPIView.as_view())
]
