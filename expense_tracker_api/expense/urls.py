from django.urls import path
from .views import ExpenseView, ExpenseDetailView

urlpatterns = [
    path("expenses/",ExpenseView.as_view(),name="expense-view"),
    path("expenses/<int:pk>/",ExpenseDetailView.as_view(),name="expense-detail-view")
]
