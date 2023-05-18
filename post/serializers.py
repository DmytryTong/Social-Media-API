from rest_framework import serializers

from .models import Post, Tag


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("id", "title", "content", "created_at", "author", "tags")


class PostListSerializer(PostSerializer):

    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")
