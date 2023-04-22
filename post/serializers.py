from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'author']

    def validate_author(self, value):
        if self.context['request'].user != value:
            raise serializers.ValidationError("You can only create posts for yourself.")
        return value
