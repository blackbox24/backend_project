from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from drf_yasg import openapi

schema = get_schema_view(
    openapi.Info(
        title="WEATHER API",
        description="Integrate external APIs and caching system",
        default_version="v1",
    ),
    permission_classes=(AllowAny,),
    public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/weather/",include("weather.urls")),
    path("docs/",schema.with_ui("swagger",cache_timeout=0),name="swagger"),
]
