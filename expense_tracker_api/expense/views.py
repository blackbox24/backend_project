from django.contrib.auth.decorators import permission_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from guardian.shortcuts import assign_perm, get_objects_for_user

from drf_yasg.utils import swagger_auto_schema
from datetime import datetime
import pytz

from drf_yasg import openapi
from config.versions import CustomVersoning
from .serializers import ExpenseSerializer
from .models import Expense
from .decorators import permission_required

import logging

logger = logging.getLogger("expense.views")

def convert_date_format(date):
    date = datetime.strptime(date,"%Y-%m-%d")
    utc_timezone = pytz.utc
    dt_with_time_and_tz = utc_timezone.localize(date.replace(hour=0, minute=0, second=0, microsecond=0))
    formatted_date = dt_with_time_and_tz.strftime("%Y-%m-%d %H:%M:%S%z")
    return formatted_date

class ExpenseView(APIView):
    versioning_class = CustomVersoning
    serializer = ExpenseSerializer
    
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('week', openapi.IN_QUERY, description="Past week", type=openapi.TYPE_STRING),
        openapi.Parameter('month', openapi.IN_QUERY, description="Past month", type=openapi.TYPE_STRING),
        openapi.Parameter('start', openapi.IN_QUERY, description="Start date", type=openapi.TYPE_STRING),
        openapi.Parameter('end', openapi.IN_QUERY, description="End date", type=openapi.TYPE_STRING)
    ])
    def get(self,request,*args, **kwargs):
        try:
            start_date = request.query_params.get("start","")
            end_date = request.query_params.get("end","")
            month = request.query_params.get("month","")
            week = request.query_params.get("week","")
            
            
            if start_date != "" and end_date != "":
                start_date =  convert_date_format(start_date)
                end_date =  convert_date_format(end_date)
                logger.info(f"start date: {start_date}")
                objects = Expense.objects.filter(
                    updated_at__range=(start_date,end_date)
                )
            elif month != "":
                objects = Expense.objects.filter(updated_at__month=month)
            elif week != "":
                objects = Expense.objects.filter(updated_at__week=week)
            else:
                objects = Expense.objects.all()

            data = get_objects_for_user(request.user,perms="expense.view_expense",klass=objects,use_groups=False,accept_global_perms=False)
            data = self.serializer(data,many=True).data
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return Response({"error":e},status=status.HTTP_400_BAD_REQUEST)
    
    
    @swagger_auto_schema(responses={201:ExpenseSerializer},request_body=ExpenseSerializer)
    def post(self,request,*args, **kwargs):
        _data = self.serializer(data=request.data)
        if _data.is_valid(raise_exception=True):
            data = _data.save()

            assign_perm("Expense.view_expense",request.user,data)
            logger.info(f"Assigned view for {_data.validated_data["name"]} object permissions to {request.user.username} ")

            assign_perm("Expense.change_expense",request.user,data)
            logger.info(f"Assigned change for {_data.validated_data["name"]} object permissions to {request.user.username} ")

            assign_perm("Expense.delete_expense",request.user,data)
            logger.info(f"Assigned delete for {_data.validated_data["name"]} object permissions to {request.user.username} ")

            return Response(_data.validated_data,status=status.HTTP_201_CREATED)
        return Response(_data.errors,status=status.HTTP_400_BAD_REQUEST)
    

class ExpenseDetailView(APIView):
    versioning_class = CustomVersoning
    serializer = ExpenseSerializer
    def fetch_expense(self,expense_id):
        try:
            return Expense.objects.get(pk=expense_id)
        except Exception as e:
            logger.inf(f"Sorry an error occurred: {e}")
            return None
        
    @permission_required
    def get(self,request,pk,*args, **kwargs):
        _object = self.fetch_expense(pk)
        if _object != None:
            serialized_data = self.serializer(_object)

            return Response(serialized_data.data,status=status.HTTP_200_OK)
        return Response({"error":"Error occurred"},status=status.HTTP_400_BAD_REQUEST)
        
    
    
    @swagger_auto_schema(responses={200:ExpenseSerializer},request_body=ExpenseSerializer)
    @permission_required
    def put(self,request,pk,*args, **kwargs):
        _object = self.fetch_expense(pk)
        if _object != None:
            data = self.serializer(_object,data=request.data)

            if data.is_valid(raise_exception=True):
                data.save()
                return Response(data.validated_data,status=status.HTTP_200_OK)
            return Response(data.errors,status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"error":"Error occurred"},status=status.HTTP_400_BAD_REQUEST)
    
    @permission_required
    def delete(self,request,pk,*args, **kwargs):
        _object = self.fetch_expense(pk)
        if _object != None:
            _object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response({"error":"Error occurred"},status=status.HTTP_400_BAD_REQUEST)