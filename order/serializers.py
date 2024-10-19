from rest_framework import serializers

from django.core.validators import MinValueValidator

from .models import Order, OrderItem

from menu.models import Menu
from menu.serializers import MenuChildSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_id = serializers.PrimaryKeyRelatedField(
        queryset=Menu.objects.all(),
        source='menu_item'
    )

    class Meta:
        model = OrderItem
        fields = ['menu_item_id', 'size', 'quantity']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("تعداد باید حداقل 1 باشد.")
        return value

    def validate_size(self, value):
        if value not in ['SMALL', 'LARGE']:
            raise serializers.ValidationError(
                "اندازه باید یکی از SMALL یا LARGE باشد.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'order_items', 'total_price', 'created_at']
        read_only_fields = ['id', 'total_price', 'created_at']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
