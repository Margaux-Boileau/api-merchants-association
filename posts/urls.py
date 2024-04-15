from django.urls import path
from .views import PostListView, PostDetailView, CommentsListView

urlpatterns = [
    path('forums/<int:forum_pk>/posts/', PostListView.as_view(), name='post-list'),
    path('forums/<int:forum_pk>/posts/<int:post_pk>', PostDetailView.as_view(), name='post-detail'),
    path('forums/<int:forum_pk>/posts/<int:post_pk>/comments/', CommentsListView.as_view(), name="forum_posts"),
]