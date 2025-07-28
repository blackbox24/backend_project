from django.contrib import admin
from .models import Todo
from guardian.models import UserObjectPermission, GroupObjectPermission
from guardian.admin import GuardedModelAdmin
# Register your models here.

@admin.register(Todo)
class TodoAdmin(GuardedModelAdmin):
    list_display = [
        "title","description","created_at"
    ]


admin.site.register(UserObjectPermission)
admin.site.register(GroupObjectPermission)