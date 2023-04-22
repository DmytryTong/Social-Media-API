from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        subscriptions = user.subscribers.all()
        return Post.objects.filter(author__in=[user] + list(subscriptions))


class CreatePost(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
