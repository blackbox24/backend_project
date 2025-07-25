from django.test import TestCase
from .models import BlogPost, Tag
from .serializers import PostSerializer, TagSerializer

# Create your tests here.
class BlogPostSerializerTests(TestCase):
    def test_valid_serializer(self):
        data = {
            "title": "Test Post",
            "content": "This is a test post.",
            "tags": [{"name": "test"}]
        }
        serializer = PostSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['title'], "Test Post")

    def test_invalid_serializer(self):
        data = {
            "title": "",
            "content": "This is a test post.",
            "tags": [{"name": "test"}]
        }
        serializer = PostSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

class TagSerializerTests(TestCase):
    def test_valid_serializer(self):
        data = {
            "name": "Test Tag"
        }
        serializer = TagSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['name'], "Test Tag")

    def test_invalid_serializer(self):
        data = {
            "name": ""
        }
        serializer = TagSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
