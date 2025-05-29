# shop/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.product_list, name='product_list'),
    path('buy/<int:product_id>/', views.buy_product, name='buy_product'),
    path('products/add/', views.add_product, name='add_product'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('return/<int:order_id>/', views.request_return, name='request_return'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
]