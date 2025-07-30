from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema = get_schema_view(
    openapi.Info(
        title="Expense Tracker API docs",
        description="Expense tracker API documentation. It includes object level permissions",
        default_version="v1",
    ),
    permission_classes=(AllowAny,),
    public=True
)

def redirect_to_doc(request):
    return redirect("swagger")

urlpatterns = [
    path('expense/', admin.site.urls),

    path("",redirect_to_doc,name="redirect-to-docs"),

    # Custom App API
    path("api/<version>/",include("expense.urls")),

    # Auth API
    path("api/v1/auth/login/",TokenObtainPairView.as_view(),name="login_view"),
    path("api/v1/auth/refresh/",TokenRefreshView.as_view(),name="refresh_token_view"),

    path("docs/",schema.with_ui("swagger",cache_timeout=0),name="swagger"),
]
