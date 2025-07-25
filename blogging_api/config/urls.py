from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema = get_schema_view(
    openapi.Info(
        title="Blogging API",
        default_version='v1',
        description="API documentation for the Blogging application",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@bloggingapi.com")
    ),
    public=True,
)

urlpatterns = [
    path('blogging/', admin.site.urls),
    
    path('swagger/', schema.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
