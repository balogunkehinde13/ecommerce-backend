from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for categories.
    Anyone can read them, only authenticated users can modify.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Enable searching and ordering by name
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
