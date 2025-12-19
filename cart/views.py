from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product


class CartView(generics.RetrieveAPIView):
    """
    Returns the authenticated user's cart.
    If the cart does not exist, it is created automatically.
    """
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


class AddToCartView(generics.CreateAPIView):
    """
    Adds a product to the user's cart.
    If the product already exists, increase its quantity.
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)

        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))

        product = get_object_or_404(Product, id=product_id)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        cart_item.quantity += quantity
        cart_item.save()

        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_200_OK
        )


class UpdateCartItemView(generics.UpdateAPIView):
    """
    Updates the quantity of a cart item.
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()


class RemoveCartItemView(generics.DestroyAPIView):
    """
    Removes a single item from the cart.
    """
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()


class ClearCartView(generics.DestroyAPIView):
    """
    Clears all items from the authenticated user's cart.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        cart.items.all().delete()

        return Response(
            {"message": "Cart cleared successfully"},
            status=status.HTTP_200_OK
        )
