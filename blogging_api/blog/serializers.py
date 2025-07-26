from rest_framework import serializers
from .models import BlogPost, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    # tags = TagSerializer(many=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'category', 'tags', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def create(self, validated_data):
        tags = validated_data.get('tags', [])
        tags_data = validated_data.pop('tags', [])
        print(tags)
        post = BlogPost.objects.create(**validated_data)
        for tag_data in tags_data:
            print(tag_data)
            tag, _ = Tag.objects.get_or_create(name=tag_data)
            post.tags.add(tag)
        return post