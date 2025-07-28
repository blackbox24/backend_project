from django.contrib import admin
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema = get_schema_view(
    openapi.Info(
        title="Todo API docs",
        description=" Todo API documentations",
        default_version="v1"
    ),
    public=True,
    permission_classes=(AllowAny,)
)

def redirect_to_docs(request:HttpRequest):
    return redirect("swagger")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",redirect_to_docs,name="redirect"),

    path("api/",include("todo.urls")),

    # auth
    path("api/auth/",include("dj_rest_auth.urls")),
    path("api/auth/register",include("dj_rest_auth.registration.urls")),

    path("docs/",schema.with_ui("swagger",cache_timeout=0),name="swagger"),
]
