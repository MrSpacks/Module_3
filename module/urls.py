# shop_project/urls.py
from django.contrib import admin
from django.urls import path, include
from app.views import return_requests_view, confirm_return  


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')), 
    path('returns/', return_requests_view, name='return_requests'),
    path('returns/confirm/<int:request_id>/', confirm_return, name='confirm_return'),
]