from django.urls import path
from .views import PostListView, PostDetailView, CommentsListView, get_post_media, delete_comment

# URLS FORUMS
# Class view implementa varios métodos http para esa url, Function view implementa uno
urlpatterns = [
    path('forums/<int:forum_pk>/posts/', PostListView.as_view(), name='posts-list'),
    path('forums/<int:forum_pk>/posts/<int:post_pk>/', PostDetailView.as_view(), name='post-detail'),
    path('forums/<int:forum_pk>/posts/<int:post_pk>/comments/', CommentsListView.as_view(), name="post-comments"),
    path('comments/<int:comment_pk>/', delete_comment, name="post-comment-detail"),
    path('forums/<int:forum_pk>/posts/<int:post_pk>/media/<str:media_pk>/', get_post_media, name="post-media"),
]