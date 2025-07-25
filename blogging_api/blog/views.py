from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BlogPost, Tag

from .serializers import PostSerializer, TagSerializer
from config.settings import logger
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
class BlogPostListView(APIView):
    @swagger_auto_schema(responses={200: PostSerializer(many=True)})
    def get(self, request):
        posts = BlogPost.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PostSerializer, responses={201: PostSerializer})
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BlogPostDetailView(APIView):
    @swagger_auto_schema(responses={200: PostSerializer})
    def get(self, request, pk):
        try:
            post = BlogPost.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BlogPost.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=PostSerializer, responses={200: PostSerializer})
    def put(self, request, pk):
        try:
            post = BlogPost.objects.get(pk=pk)
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
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BlogPost.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
class TagListView(APIView):
    @swagger_auto_schema(responses={200: TagSerializer(many=True)})
    def get(self, request):
        tags = Tag.objects.all()
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
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Tag.DoesNotExist:
            return Response({"error": "Tag not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(responses={204: "No Content"})
    def delete(self, request, pk):
        try:
            tag = Tag.objects.get(pk=pk)
            tag.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Tag.DoesNotExist:
            return Response({"error": "Tag not found"}, status=status.HTTP_404_NOT_FOUND)
    