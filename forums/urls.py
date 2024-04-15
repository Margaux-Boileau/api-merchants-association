from django.urls import path
from . import views

urlpatterns = [
    path('forums/all/', views.forum_get_all_view, name='forum_get_all'),
    path('forums/', views.forum_post_view, name='forum_post'),
    path('forums/<int:pk>/', views.forum_detail_view, name="forum_detail"),
]