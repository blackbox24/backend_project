from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from .models import BlogPost, Tag

from .serializers import PostSerializer, TagSerializer
from config.settings import logger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class BlogPostListView(APIView):
    @swagger_auto_schema(responses={200: PostSerializer(many=True)}, manual_parameters=[
        openapi.Parameter('terms', openapi.IN_QUERY, description="Search terms for blog posts", type=openapi.TYPE_STRING)
    ])
    def get(self, request):
        terms = request.query_params.get("terms", "")
        if terms != "" and cache.get(f'blog_posts:{terms}'):
            posts = cache.get(f'blog_posts:{terms}')
            logger.info("Cache hit for blog posts with search terms")
        elif terms != "" and cache.get(f'blog_posts:{terms}') is None:
            posts = BlogPost.objects.filter(title__icontains=terms).prefetch_related('tags')
            cache.set(f'blog_posts:{terms}', posts, 60 * 15)
            logger.info("Cache updated for blog posts with search terms")
        elif terms == "" and cache.get('blog_posts') != None: 
            logger.info("Cache hit for blog posts")
            posts = cache.get('blog_posts')
        else:
            posts = BlogPost.objects.prefetch_related('tags').all()
            cache.set('blog_posts', posts, 60 * 15)
            logger.info("Cache updated for all blog posts")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PostSerializer, responses={201: PostSerializer})
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.set('blog_posts', None)
            logger.info("Cache invalidated for blog posts")
            # cache.delete('blog_posts')  # Invalidate cache for all posts
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BlogPostDetailView(APIView):
    @swagger_auto_schema(responses={200: PostSerializer})
    def get(self, request, pk):

        try:
            post = BlogPost.objects.get(pk=pk)
            cache.set(f'blog_post_{pk}', post, 60 * 15)
            cache.set('blog_posts', None)  # Invalidate cache for all posts
            logger.info(f"Cache updated for blog post {pk}")

            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BlogPost.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=PostSerializer, responses={200: PostSerializer})
    def put(self, request, pk):
        try:
            post = BlogPost.objects.get(pk=pk)
            cache.set(f'blog_post_{pk}', post, 60 * 15)
            cache.set('blog_posts', None)  # Invalidate cache for all posts
            logger.info(f"Cache updated for blog post {pk}")

            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BlogPost.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(responses={204: "No Content"})
    def delete(self, request, pk):
        try:
            post = BlogPost.objects.get(pk=pk)
            post.delete()

            cache.set('blog_posts', None)  # Invalidate cache for all posts
            logger.info(f"Cache invalidated for blog post {pk}")
            cache.delete(f'blog_post_{pk}')

            return Response(status=status.HTTP_204_NO_CONTENT)
        except BlogPost.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
class TagListView(APIView):
    @swagger_auto_schema(responses={200: TagSerializer(many=True)})
    def get(self, request):
        if cache.get('tags'):
            logger.info("Cache hit for tags")
            tags = cache.get('tags')
        else:
            tags = Tag.objects.all()
            cache.set('tags', tags, 60 * 15)
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=TagSerializer, responses={201: TagSerializer})
    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TagDetailView(APIView):
    @swagger_auto_schema(responses={200: TagSerializer})
    def get(self, request, pk):
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tag.DoesNotExist:
            return Response({"error": "Tag not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=TagSerializer, responses={200: TagSerializer})
    def put(self, request, pk):
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag, data=request.data)
            if serializer.is_valid():
                serializer.save()
                cache.set(f'tag_{pk}', tag, 60 * 15)
                logger.info(f"Cache updated for tag {pk}")
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Tag.DoesNotExist:
            return Response({"error": "Tag not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(responses={204: "No Content"})
    def delete(self, request, pk):
        try:
            tag = Tag.objects.get(pk=pk)
            tag.delete()
            cache.set('tags', None)  # Invalidate cache for all tags
            logger.info(f"Cache invalidated for tag {pk}")
            cache.delete(f'tag_{pk}')
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Tag.DoesNotExist:
            return Response({"error": "Tag not found"}, status=status.HTTP_404_NOT_FOUND)
    