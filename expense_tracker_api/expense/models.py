from django.db import models

class BaseTimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

class Category(BaseTimestampedModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

# Create your models here.
class Expense(BaseTimestampedModel):
    name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=3,decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['name']),
        ]