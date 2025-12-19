from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Wishlist, Product
from .serializers import WishlistSerializer


class WishlistView(generics.ListAPIView):
    """
    Returns all products in the user's wishlist.
    """
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


class AddToWishlistView(generics.CreateAPIView):
    """
    Adds a product to the wishlist.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product')
        product = get_object_or_404(Product, id=product_id)

        Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )

        return Response(
            {"message": "Product added to wishlist"},
            status=status.HTTP_201_CREATED
        )


class RemoveFromWishlistView(generics.DestroyAPIView):
    """
    Removes a product from the wishlist.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        wishlist_item = get_object_or_404(
            Wishlist,
            user=request.user,
            product_id=product_id
        )
        wishlist_item.delete()

        return Response(
            {"message": "Product removed from wishlist"},
            status=status.HTTP_200_OK
        )
