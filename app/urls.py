# shop/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.product_list, name='product_list'),
    path('buy/<int:product_id>/', views.buy_product, name='buy_product'),
]