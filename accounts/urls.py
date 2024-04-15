from django.urls import path
from . import views

urlpatterns = [
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/<str:username>/', views.account_detail_view, name='shop'),
    path('accounts/<str:username>/changepassword/', views.account_change_password_view, name='change_assword'),
]
