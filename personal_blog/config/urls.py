from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('personal_blog/', admin.site.urls),
    path("",include("pages.urls")),
]
