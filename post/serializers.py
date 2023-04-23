from rest_framework import serializers

from user.serializers import UserSerializer
from .models import Post, Tag


class PostSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = Post
        fields = ["id", "author", "title", "content", "created_at", "tags"]


class PostListSerializer(PostSerializer):
    tags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")
