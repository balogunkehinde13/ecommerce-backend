from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Displays all items belonging to an order on the Order admin page.
    """
    model = OrderItem
    extra = 0  # No empty rows unless needed
    readonly_fields = ['price_at_purchase', 'quantity', 'subtotal']



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for Orders.
    Shows:
    - order ID
    - user
    - status
    - total price
    - creation date
    """

    list_display = [
        'id', 'user', 'status',
        'total_price', 'created_at'
    ]

    list_filter = [
        'status',
        'created_at'
    ]

    search_fields = [
        'user__username',
        'id'
    ]

    inlines = [OrderItemInline]

    readonly_fields = [
        'total_price', 'created_at'
    ]



@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    View OrderItems independently as well.
    """

    list_display = [
        'order',
        'product',
        'quantity',
        'price_at_purchase',
        'subtotal'
    ]

    readonly_fields = ['subtotal']
