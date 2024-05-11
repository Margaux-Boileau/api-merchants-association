from . import views
from django.urls import path

# URLS SHOPS
# Class view implementa varios métodos http para esa url, Function view implementa uno
urlpatterns = [
    path('shops/', views.ShopListView.as_view(), name="shops"),
    path('shops/<str:pk>/', views.ShopDetailView.as_view(), name="shop_detail"),
    path('shops/<str:pk>/employees/', views.ShopEmployeesView.as_view(), name="shop_employees"),
    path('shops/<str:pk>/forums/', views.get_shop_forums_view, name="shop_get_forums"),
    path('shops/<str:pk>/image/', views.get_shop_image_view, name="get_shop_image_view"),
]