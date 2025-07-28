from rest_framework.permissions import BasePermission
from guardian.core  import ObjectPermissionChecker

class IsOwnerPerm(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.has_perm("todo.view_todo") and request.user.has_perm("todo.add_todo"):
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        checker = ObjectPermissionChecker(request.user)
        # if request.
        if request.method in ['GET']:
            return checker.has_perm('todo.view_todo', obj) 
               
        if request.method in ['POST']:
            return checker.has_perm('todo.add_todo', obj)
        
        if request.method in ['PUT', 'PATCH']:
            return checker.has_perm('todo.change_todo', obj)
        
        if request.method in ['DELETE']:
            return checker.has_perm('todo.delete_todo', obj)
