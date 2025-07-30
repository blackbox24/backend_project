from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN
from guardian.core import ObjectPermissionChecker
from .models import Expense

def permission_required(view_func):
    def wrapper(request,*args, **kwargs):
        pk = kwargs.get("pk")
        obj = Expense.objects.get(pk=pk)
        check = ObjectPermissionChecker(request.request.user)
        if check.has_perm("view_expense",obj) or \
            check.has_perm("change_expense",obj) or \
            check.has_perm("delete_expense",obj):
            return view_func(request,*args, **kwargs)
        return Response({"error":"Permission denied"},status=HTTP_403_FORBIDDEN)
    return wrapper