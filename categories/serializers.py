from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializes categories.
    Includes a dynamic field `product_count`
    showing how many products belong to each category.
    This improves API usefulness without extra queries.
    """
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'description',
            'product_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_product_count(self, obj):
        """
        Count products inside the category.
        """
        return obj.products.count()
