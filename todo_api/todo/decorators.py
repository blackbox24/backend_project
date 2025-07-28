from guardian.core import ObjectPermissionChecker
from rest_framework.response import Response
from rest_framework import status
from .models import Todo

def permission_required(view_func):
    def wrapper(request,*args,**kwargs):
        pk = kwargs.get("pk")
        user = request.request.user
        checker = ObjectPermissionChecker(user)
        obj = Todo.objects.get(id=pk)
        
        if request.get and checker.has_perm("todo.view_todo",obj=obj):
            return view_func(request,*args,**kwargs)
        elif request.put and checker.has_perm("todo.change_todo",obj=obj):
            return view_func(request,*args,**kwargs)
        return Response({"error":"access denied"},status=status.HTTP_403_FORBIDDEN)
    return wrapper
