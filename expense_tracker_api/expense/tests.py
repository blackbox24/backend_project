from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from django.urls import reverse
from django.contrib.auth import get_user_model, models
from guardian.shortcuts import assign_perm

from .models import Expense
from .serializers import ExpenseSerializer
from config.settings import logger

User = get_user_model()
# Create your tests here.
class DefaultTestCase(APITestCase):
    def setUp(self):
        # create user
        self.user = User.objects.create_user(username="testuser1",email="testuser@example.com", password="testpass123")
        # create expense
        expense = Expense.objects.create(name="item 1",amount=8.01)
        Expense.objects.create(name="item 1",amount=2.00)
        Expense.objects.create(name="item 1",amount=1.00)

        # asssign perm to user
        self.user.user_permissions.set(
            models.Permission.objects.filter(codename__icontains="expense")
        )

        for action in ["view","change","delete"]:
            assign_perm(perm=f"expense.{action}_expense",user_or_group=self.user,obj=expense)
        
        # authenticate
class AuthenticatedTestSetup(DefaultTestCase):
    def setUp(self):
        super().setUp()
        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}") 

class AuthenticatedViewTest(AuthenticatedTestSetup):
    
    def test_expense_list_view(self):
        response = self.client.get(reverse("expense-view",args=["v1"]))

        self.assertEqual(response.status_code,200)

# CRUD expense test
class CrudExpenseView(AuthenticatedTestSetup):
    
    def test_create_expense(self):
        response = self.client.post(
            reverse("expense-view",args=["v1"]),
            data={"name":"test item","amount":"2.01"}
        )

        self.assertTrue(response.status_code == 201)

    def test_read_expense_url(self):
        response = self.client.get(
            reverse("expense-view",args=["v1"]),
        )

        self.assertTrue(response.status_code == 200)
        self.assertTrue(len(response.json()) > 0 and len(response.json()) == 1)
    
    def test_retrieve_expense_view(self):
        url = reverse("expense-detail-view",kwargs={"version":"v1","pk":1})
        response = self.client.get(url)
        data = response.json()

        logger.info(f"url :{url}")
        logger.info(f"data :{data}")
        self.assertEqual(data.get("name"), "item 1")
        self.assertEqual(data.get("amount"), "8.01")
        self.assertEqual(response.status_code, 200)
    
    def test_retrieve_no_perm_expense_view(self):
        url = reverse("expense-detail-view",kwargs={"version":"v1","pk":2})
        response = self.client.get(url)

        logger.info(f"url :{url}")
        self.assertEqual(response.status_code, 403)

    def test_remove_perm_expense_view(self):
        url = reverse("expense-detail-view",kwargs={"version":"v1","pk":1})
        response = self.client.delete(url)

        logger.info(f"url :{url}")
        self.assertEqual(response.status_code, 204)
        # self.assertTrue(len(response.json()) > 0 and len(response.json()) == 1)

# Model and Object Permissions test
