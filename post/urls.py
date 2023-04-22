from django.urls import path
from .views import PostList, CreatePost

app_name = 'posts'

urlpatterns = [
    path('post_list/', PostList.as_view(), name='post_list'),
    path('create_post/', CreatePost.as_view(), name='create_post'),
]