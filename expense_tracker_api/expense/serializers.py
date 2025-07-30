from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [
            "id","name","amount","created_at","updated_at"
        ]
        extra_kwargs = {
            "id":{"required":False,"read_only":True},
            "created_at":{"required":False,"read_only":True},
             "updated_at":{"required":False,"read_only":True},
        }