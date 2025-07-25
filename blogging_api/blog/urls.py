from django.urls import path
from .views import BlogPostListView, BlogPostDetailView, TagListView, TagDetailView

urlpatterns = [
    # BlogPost URLs
    path('posts/', BlogPostListView.as_view(), name='blogpost-list'),
    path('posts/<int:pk>/', BlogPostDetailView.as_view(), name='blogpost-detail'),

    # Tag URLs
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tags/<int:pk>/', TagDetailView.as_view(), name='tag-detail'),
]