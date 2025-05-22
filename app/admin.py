from django.contrib import admin
from .models import CustomUser, Product, Order, ReturnRequest
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(ReturnRequest)