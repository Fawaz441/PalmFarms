from django.urls import path
from .views import speech_recognition

urlpatterns = [
    path('speech', speech_recognition, name='speech_recognition')
]
