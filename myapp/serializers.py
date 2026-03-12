from rest_framework import serializers
from .models import FoodItem, Order, OrderItem

class KitchenOrderItemSerializer(serializers.ModelSerializer):
    food_name = serializers.CharField(source="food_item.name")

    class Meta:
        model = OrderItem
        fields = ["food_name", "quantity"]


class KitchenOrderSerializer(serializers.ModelSerializer):
    items = KitchenOrderItemSerializer(source="orderitem_set", many=True)

    class Meta:
        model = Order
        fields = ["id", "table_number", "status", "order_time", "items"]

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["food_item", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ["id", "customer_name", "table_number", "items"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)

        for item in items_data:
            OrderItem.objects.create(order=order, **item)

        return order