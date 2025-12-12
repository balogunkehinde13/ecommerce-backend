from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """
    Represents a single item in the cart.
    Includes nested ProductSerializer for better API detail.
    """
    product_details = ProductSerializer(source="product", read_only=True)

    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'product_details',
            'quantity', 'subtotal'
        ]
        read_only_fields = ['id', 'subtotal', 'product_details']



class CartSerializer(serializers.ModelSerializer):
    """
    Represents an entire cart with its items.
    Useful for showing:
    - Cart total
    - Item details
    - Item quantities
    """
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id', 'user', 'items',
            'total_items', 'total_price',
            'created_at'
        ]
        read_only_fields = [
            'id', 'user', 'total_items',
            'total_price', 'created_at'
        ]
