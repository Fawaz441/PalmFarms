from django.urls import path
from .views import get_user_details, submit_contact_message

urlpatterns = [
    path('get-user-details', get_user_details, name='get_user_details'),
    path('submit', submit_contact_message, name='submit')
]
