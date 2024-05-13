from django.urls import path
from .views import get_post_media_view, get_logo

urlpatterns = [
    path('forums/<int:forum_pk>/posts/<int:post_pk>/media/<str:media_pk>/', get_post_media_view, name='get_post_media_view'),
    path('media/logo/', get_logo, name='get_logo'),
]