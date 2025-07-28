from rest_framework.views import APIView
from guardian.shortcuts import assign_perm, get_objects_for_user
from guardian.decorators import permission_required_or_404
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Todo
from .serializers import TodoSerializer
from .permissions import IsOwnerPerm
from .decorators import permission_required

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TodoView(APIView):
    permission_classes = (IsOwnerPerm,)
    serializer = TodoSerializer
    queryset = Todo

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Search terms for blog posts", type=openapi.TYPE_STRING)
    ])
    def get(self,request,*args,**kwargs):
        search = request.query_params.get("search","")
        logger.info("fetched todos")
        if search:
            data = self.queryset.objects.filter(title__icontains=search)
        else:
            data = self.queryset.objects.all()
        serialized_data = TodoSerializer(
            get_objects_for_user(
                user=request.user,
                perms="todo.view_todo",
                klass=data,
                use_groups=False,
                accept_global_perms=False
            ),
            many=True
        ).data
        
        return Response(data=serialized_data,status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=TodoSerializer)
    def post(self,request,*args,**kwargs):
        serialized_data = TodoSerializer(data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            data = serialized_data.save()
            logger.info(f"Created todo {serialized_data.validated_data['title']}")

            assign_perm("todo.view_todo",request.user,obj=data)
            assign_perm("todo.change_todo",request.user,obj=data)
            assign_perm("todo.delete_todo",request.user,obj=data)
            logger.info(f"Assigned todo RUD perms for {serialized_data.validated_data['title']} to {request.user.username}")

            return Response(serialized_data.validated_data,status=status.HTTP_201_CREATED) 
        return Response({"error":"Failed to save todo"},status=status.HTTP_400_BAD_REQUEST)
    
class TodoDetailView(APIView):
    permission_classes = (IsOwnerPerm,)
    serializer = TodoSerializer
    queryset = Todo

    def fetch_object(self,pk):
        try:
            logger.info(f"get todo {pk}")
            return self.queryset.objects.get(id=pk)
        except Exception as e:
            logger.info(f"Error occurried {e}")
            return None

    @permission_required
    def get(self,request,pk,*args,**kwargs):
        data = self.fetch_object(pk=pk)
        if data != None:
            serialized_data = TodoSerializer(data)
            return Response(data=serialized_data.data,status=status.HTTP_200_OK)
        return Response({"error":"Error occurred"},status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(request_body=TodoSerializer, responses={200: TodoSerializer})
    @permission_required
    def put(self,request,pk,*args,**kwargs):
        data = self.fetch_object(pk=pk)

        if data != None:
            serialized_data = TodoSerializer(data,data=request.data)
            if serialized_data.is_valid(raise_exception=True):
                serialized_data.save()
                return Response(serialized_data.validated_data,status=status.HTTP_204_NO_CONTENT) 
            return Response({"error":"Failed to save todo"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"error":"data cannot be found"},status=status.HTTP_404_NOT_FOUND) 