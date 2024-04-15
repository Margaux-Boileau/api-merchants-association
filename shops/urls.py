from .views import ShopListView, ShopDetailView, ShopEmployeesView, get_shop_forums_view
from django.urls import path

urlpatterns = [
    path('shops/', ShopListView.as_view(), name="shops"),
    path('shops/<str:pk>', ShopDetailView.as_view(), name="shop_detail"),
    path('shops/<str:pk>/employees/', ShopEmployeesView.as_view(), name="shop_employees"),
    path('shops/<str:pk>/forums', get_shop_forums_view, name="shop_get_forums"),
]