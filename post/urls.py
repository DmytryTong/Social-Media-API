from django.urls import path, include
from rest_framework import routers

from .views import TagViewSet, PostViewSet

app_name = "post"

router = routers.DefaultRouter()
router.register("tags", TagViewSet)
router.register("posts", PostViewSet)

urlpatterns = [
    path("", include(router.urls))
]
