from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Order, OrderItem
from cart.models import Cart, CartItem
from products.models import Product
from .serializers import OrderSerializer


class CreateOrderView(generics.CreateAPIView):
    """
    Creates a new order from the authenticated user's cart.
    Steps:
      1. Get user cart
      2. Ensure cart is not empty
      3. Create new Order instance
      4. Copy CartItems → OrderItems
      5. Deduct stock quantities
      6. Compute order total
      7. Clear cart
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Retrieve the user’s cart. If not found → 404
        cart = get_object_or_404(Cart, user=request.user)
        items = cart.items.all()

        # Prevent creating empty orders
        if not items.exists():
            return Response(
                {"error": "Your cart is empty."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the main Order object
        order = Order.objects.create(user=request.user)

        # Loop through cart items and convert each into an OrderItem
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_at_purchase=item.product.price  # Save price snapshot
            )

            # Deduct purchased quantity from product stock
            item.product.stock_quantity -= item.quantity
            item.product.save()

        # Calculate and store the total price
        order.calculate_total()

        # Clear cart after successful order creation
        cart.items.all().delete()

        # Return detailed order data to the client
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )



class OrderListView(generics.ListAPIView):
    """
    Returns a list of all orders that belong to the authenticated user.

    Example:
      GET /api/orders/
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return orders belonging to the logged-in user
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
