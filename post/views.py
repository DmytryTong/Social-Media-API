from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .models import Post, Tag
from .serializers import PostSerializer, PostListSerializer, TagSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all().prefetch_related("tags")
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    @staticmethod
    def _params_to_ints(params):
        return [int(str_id) for str_id in params.split(",")]

    def get_queryset(self):
        subscribers_ids = (
            self.request.user.profile.subscribers.all()
        )
        user_id = self.request.user.profile.id

        queryset = self.queryset.filter(
            author__in=list(subscribers_ids) + [user_id]
        )
        tags = self.request.query_params.get("tags")
        if tags:
            tags_ids = self._params_to_ints(tags)
            queryset = (queryset.filter(tags__id__in=tags_ids))
        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "tags",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by tags id (ex. ?tags=1,2)"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
