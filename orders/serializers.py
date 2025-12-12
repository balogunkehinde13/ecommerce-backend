from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Represents a single product inside an order.
    Includes:
    - Price at purchase
    - Quantity
    - Subtotal (calculated dynamically)
    """
    product_details = ProductSerializer(source="product", read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_details',
            'quantity', 'price_at_purchase',
            'subtotal'
        ]
        read_only_fields = ['id', 'subtotal', 'product_details']



class OrderSerializer(serializers.ModelSerializer):
    """
    Serializes entire orders including nested items.
    Shows:
    - User
    - Status
    - Total price
    - Item breakdown
    """
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'status',
            'total_price', 'total_items',
            'created_at', 'items'
        ]
        read_only_fields = [
            'id', 'user', 'total_price',
            'total_items', 'created_at'
        ]
