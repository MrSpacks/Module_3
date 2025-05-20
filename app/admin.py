from django.contrib import admin

from .models import CustomUser, Product, Order, ReturnRequest

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'balance')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')
    ordering = ('username',)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    search_fields = ('name',)
    list_filter = ('price',)
    ordering = ('name',)
class OrderAdmin(admin.ModelAdmin): 
    list_display = ('user', 'product', 'created_at', 'status')
    search_fields = ('user__username', 'product__name')
    list_filter = ('status',)
    ordering = ('-created_at',)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ('order', 'requested_at', 'reason')
    search_fields = ('order__user__username', 'order__product__name')
    list_filter = ('requested_at',)
    ordering = ('-requested_at',)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ReturnRequest, ReturnRequestAdmin)