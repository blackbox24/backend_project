from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from expense.models import Expense,Category

from guardian.shortcuts import assign_perm
from django.contrib.auth import get_user_model
from random import randint, choice

User = get_user_model();

class Command(BaseCommand):
    help = "Seed database"

    def create_users(self,username,email,password,is_superuser=False):
        user,_created = User.objects.get_or_create(
            username=username,email=email,is_active=True
        )
        if not _created:
            self.stdout.write(self.style.ERROR(f"{user.username} already exists"))

        elif _created and is_superuser:
            user.set_password(password)
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f"{user.username} succesfully created"))

        else:
            user.set_password(password)
            user.user_permissions.set(
                objs=Permission.objects.filter(codename__icontains="expense")
            )
            user.save()
            self.stdout.write(self.style.SUCCESS(f"{user.username} succesfully created"))

        return user

    def create_category(self,cats):
        for cat in cats:
            obj, created = Category.objects.get_or_create(name=cat)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully created {cat}"))
            else:
                self.stdout.write(self.style.ERROR(f"{cat} Already exists"))

    def handle(self, *args, **options):
        # create users
        no_users = randint(4,8)
        no_expenses = randint(3,7)
        cats = ["Groceries","Leisure","Electronics","Utilities","Clothing","Health","Others"]
        self.create_category(cats)

        for i in range(0,no_users):
            user = self.create_users(username=f"testuser{i}",email=f"testuser{i}@example.com",password="testpass123")
            for x in range(0,no_expenses):
                category, _ = Category.objects.get_or_create(name=choice(cats))
                obj = Expense.objects.create(
                    name=f"test_item{x}",
                    amount=2.00,
                    category=category
                )

                assign_perm("Expense.change_expense",user,obj)
                assign_perm("Expense.view_expense",user,obj)
                assign_perm("Expense.delete_expense",user,obj)
                self.stdout.write(self.style.SUCCESS(f"assigned view, change and delete perm for {obj.name} to {user.username}"))
        self.create_users(username="testuser",email="testuser@example.com",password="testpass123",is_superuser=True)
    
        # self.stdout.write(self.style.SUCCESS("Successfully seeded database"))