from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.settings import api_settings

from user.filters import UserFilter
from user.serializers import UserSerializer, AuthTokenSerializer, UserListSerializer, UserDetailSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserList(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    filterset_fields = ["email"]
    fields = ["email"]


class UserDetail(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    queryset = get_user_model().objects.all()
    lookup_field = 'id'


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class SubscribeView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        subscriber = request.user

        # Перевірте, чи не підписується користувач на себе
        if subscriber == user:
            return Response({"error": "Can't subscribe to yourself"}, status=status.HTTP_400_BAD_REQUEST)

        # Перевірте, чи вже підписався користувач на цього користувача
        if subscriber.subscriptions.filter(id=user.id).exists():
            return Response({"error": "Already subscribed"}, status=status.HTTP_400_BAD_REQUEST)

        subscriber.subscriptions.add(user)
        serializer = self.get_serializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

