from django.urls import path
from .views import get_data

urlpatterns = [
    path("<str:country>/",get_data,name="get_weather_data"),
]