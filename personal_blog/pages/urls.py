from django.urls import path,  include
from django.contrib.auth import urls as django_auth_urls
from .views import home_page, article_page, dashboard, add_blog_page, edit_blog_page, delete_blog_page

app_name = "pages"

urlpatterns = [
    path("", home_page, name="index"), 
    path("home", home_page, name="index"), 

    path("new", add_blog_page, name="new"), 

    path("article/<int:pk>", article_page, name="article"), 
    path("edit/<int:pk>", edit_blog_page, name="edit"), 
    path("delete/<int:pk>", delete_blog_page, name="delete"), 

    # Dashboard
    path("admin", dashboard, name="admin"), 

    # Auth
    path("account/", include(django_auth_urls)), 
]