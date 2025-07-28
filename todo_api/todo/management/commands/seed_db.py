from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from guardian.shortcuts import assign_perm
from todo.models import Todo
from random import choice, randint
User = get_user_model()

class Command(BaseCommand):
    def create_user(self,username,email,password,superuser=False):
        user, created = User.objects.get_or_create(username=username,email=email)
        if not created:
            self.stdout.write(self.style.ERROR(f"{user.username} is already available"))
        else:
            if superuser:
                user.is_superuser = True
                user.is_staff = True
            
            user.set_password(password)
            user.save()

            self.assign_model_perms(user)
            self.stdout.write(self.style.SUCCESS(f"Successfully created {user.username}, superuser: {superuser}"))
        return user
    
    def assign_model_perms(self,user):
        try:
            for perm in ["view","change","add","delete"]:
                # model perms
                user.user_permissions.add(
                    Permission.objects.get(codename=f"{perm}_todo")
                )
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Successfully set {perm} for model todo"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(e))

    
    def assign_obj_perms(self,user,obj):
        for perm in ["view","change","delete"]:
            # object perms
            assign_perm(f"todo.{perm}_todo",user,obj)
            self.stdout.write(self.style.SUCCESS(f"Successfully set {perm} for model todo"))

    def handle(self, *args, **options):
        n = 4
        for user_no in range(n):
            n_todos = randint(3,8)
            if user_no != n -1:
                user = self.create_user(
                    username=f"testuser{user_no}",
                    email=f"testuser{user_no}@mail.com",
                    password="testpass123",
                    superuser=False
                )
            else:
                user = self.create_user(
                    username=f"testuser{user_no}",
                    email=f"testuser{user_no}@mail.com",
                    password="testpass123",
                    superuser=True
                )
            for i in range(n_todos*user_no,n_todos*(user_no + 1)):
                obj, created = Todo.objects.get_or_create(
                    title=f"Title of book {i}",
                    description=f"I must do number {i}"
                )
                if not created:
                    self.stdout.write(self.style.ERROR(f"{obj.title} already exists"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"successfully created {obj.title}"))
                    self.assign_obj_perms(
                        user=user,
                        obj=obj
                    )
