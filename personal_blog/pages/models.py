from django.db import models

# Create your models here.
class BaseTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Blog(BaseTimeModel):
    title = models.CharField(max_length=50, null=False)
    content = models.TextField()

    def __str__(self):
        return self.title
    