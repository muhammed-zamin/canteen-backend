from django.contrib import admin
from .models import FoodItem, Order, OrderItem


class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'is_available')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'table_number', 'status', 'order_time')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'food_item', 'quantity')


admin.site.register(FoodItem, FoodItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)