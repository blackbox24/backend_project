from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from decouple import config
from drf_yasg.utils import swagger_auto_schema
from config.settings import logger
from django.core.cache import cache

import requests

API_KEY = config("WEATHER_API_KEY",cast=str)

@api_view(["GET"])
@swagger_auto_schema()
def get_data(request,country):
    base_url = config("WEATHER_BASE_API",cast=str)
    url = f"{base_url}{country}?key={API_KEY}"

    if cache.get(country):
        logger.info(f"Cache {country}")
        return Response(data=cache.get(country),status=status.HTTP_200_OK)
    else:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            cache.set(country,data)

            logger.info(f"STATUS CODE {response.status_code}")
            logger.info(f"URL: {url}")

            return Response(data=data,status=status.HTTP_200_OK)

    return Response("error",status=response.status_code)
