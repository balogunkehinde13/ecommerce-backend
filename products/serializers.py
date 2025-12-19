from rest_framework import serializers
from .models import Product, Review, Wishlist
from categories.serializers import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for reading product data.
    Includes:
    - Category name
    - Creator username
    - Computed field: in_stock
    """

    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )

    created_by_username = serializers.CharField(
        source='created_by.username',
        read_only=True
    )

    in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price',

            'category',            # category ID
            'category_name',       # readable name

            'stock_quantity',
            'image_url', 'image',

            'created_date', 'updated_date',
            'created_by', 'created_by_username',

            'is_available', 'in_stock'
        ]

        read_only_fields = [
            'id', 'created_date', 'updated_date',
            'created_by', 'created_by_username',
            'category_name', 'in_stock'
        ]

    # Validation ensures clean data BEFORE DB save
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value



class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Smaller serializer used for:
    - POST (create)
    - PUT/PATCH (update)
    Does NOT expose read-only fields like:
    - created_by
    - in_stock
    """

    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price',
            'category', 'stock_quantity',
            'image_url', 'image', 'is_available'
        ]

    def validate_name(self, value):
        """
        Protects against extremely short or meaningless names.
        """
        if len(value) < 3:
            raise serializers.ValidationError("Product name must be at least 3 characters long.")
        return value

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for product reviews.
    """
    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = [
            'id',
            'rating',
            'comment',
            'username',
            'created_at'
        ]
        read_only_fields = ['id', 'username', 'created_at']

class WishlistSerializer(serializers.ModelSerializer):
    """
    Serializer for wishlist items.
    """
    product_details = ProductSerializer(
        source='product',
        read_only=True
    )

    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'product_details', 'created_at']
        read_only_fields = ['id', 'created_at', 'product_details']
