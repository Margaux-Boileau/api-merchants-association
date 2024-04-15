from django.urls import path
from .views import MediaListAPIView, MediaDetailAPIView

urlpatterns = [
    path('media/', MediaListAPIView.as_view(), name='media-list'),
    path('media/<int:pk>/', MediaDetailAPIView.as_view(), name='media-detail'),
]