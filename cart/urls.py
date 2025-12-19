from django.urls import path
from .views import (
    CartView,
    AddToCartView,
    UpdateCartItemView,
    RemoveCartItemView,
    ClearCartView
)

urlpatterns = [
    # View the current user's cart
    path('', CartView.as_view(), name='cart'),

    # Add product to cart
    path('add/', AddToCartView.as_view(), name='cart-add'),

    # Update quantity of a cart item
    path('item/<int:pk>/update/', UpdateCartItemView.as_view(), name='cart-item-update'),

    # Remove a single item from cart
    path('item/<int:pk>/remove/', RemoveCartItemView.as_view(), name='cart-item-remove'),

    # Clear entire cart
    path('clear/', ClearCartView.as_view(), name='cart-clear'),
]
