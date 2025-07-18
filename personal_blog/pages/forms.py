from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    published_at = forms.DateField()
    class Meta:
        model = Blog
        fields = [
            "title","content","published_at"
        ]
        extra_kwargs = {
            "title": {"required":True},
            "content": {"required": True},
            "published_at": {"required": False, "read_only":True}
        }