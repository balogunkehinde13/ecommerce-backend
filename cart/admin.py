from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """
    Shows CartItems inside the Cart page in admin.
    Much easier for admins to inspect cart contents.
    """
    model = CartItem
    extra = 0  # Do not show extra empty rows by default



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Admin interface for viewing carts.
    """

    list_display = [
        'id',
        'user',
        'total_items',
        'total_price',
        'created_at'
    ]

    inlines = [CartItemInline]  # Embed CartItems in Cart page

    readonly_fields = [
        'total_items', 'total_price', 'created_at'
    ]



@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """
    Standalone view of cart items.
    """

    list_display = [
        'cart',
        'product',
        'quantity',
        'subtotal'
    ]

    readonly_fields = ['subtotal']
