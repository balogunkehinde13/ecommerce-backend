from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Controls how Product objects appear in the Django admin panel.
    Helps admins quickly inspect:
    - product name
    - category
    - pricing
    - availability
    - stock levels
    """

    list_display = [
        'name', 'category', 'price',
        'stock_quantity', 'is_available',
        'created_date'
    ]

    # Useful filters in admin sidebar
    list_filter = [
        'category', 'is_available',
        'created_date'
    ]

    # Search bar at the top of the product list page
    search_fields = [
        'name', 'description'
    ]

    # Allow admin to edit these fields directly from list page
    list_editable = [
        'price', 'stock_quantity', 'is_available'
    ]

    # Prevent changing these fields manually
    readonly_fields = [
        'created_date', 'updated_date', 'created_by'
    ]
