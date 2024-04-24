from django.urls import path
from . import views

urlpatterns = [
    path('forums/all/', views.forum_get_all_view, name='get-all-forums'),
    path('forums/', views.forum_post_view, name='post-forum'),
    path('forums/<int:pk>/', views.forum_detail_view, name="get-forum-detail"),
]