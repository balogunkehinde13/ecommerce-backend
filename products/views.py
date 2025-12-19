from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Product, Review
from .serializers import ProductSerializer, ProductCreateUpdateSerializer, ReviewSerializer
from .filters import ProductFilter


class ProductViewSet(viewsets.ModelViewSet):
    """
    Main viewset for managing products.

    Features:
    - CRUD operations
    - Search (name, description, category)
    - Filtering (price range, category, availability)
    - Ordering (price, name, date created)
    """
    queryset = Product.objects.select_related('category', 'created_by').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    permission_classes = [IsAuthenticatedOrReadOnly]

    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['price', 'name', 'created_date', 'stock_quantity']
    ordering = ['-created_date']

    def get_serializer_class(self):
        """
        Use a smaller serializer for create/update,
        and a full serializer for GET requests.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        """
        Automatically attach the user who created the product.
        """
        serializer.save(created_by=self.request.user)

    # -----------------------------------------
    # CUSTOM ENDPOINTS
    # -----------------------------------------

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Advanced search endpoint.
        Supports multiple query parameters:
        - q (text search)
        - category
        - min_price
        - max_price
        """
        query = request.query_params.get("q", "")
        products = self.get_queryset()

        if query:
            products = products.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )

        category = request.query_params.get("category")
        if category:
            products = products.filter(category__name__iexact=category)

        min_price = request.query_params.get("min_price")
        if min_price:
            products = products.filter(price__gte=min_price)

        max_price = request.query_params.get("max_price")
        if max_price:
            products = products.filter(price__lte=max_price)

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(self.get_serializer(products, many=True).data)

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """
        Get all products belonging to a specific category.
        Example: /products/by_category/?name=Electronics
        """
        category_name = request.query_params.get("name")

        if not category_name:
            return Response({"error": "Category name is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        products = self.get_queryset().filter(category__name__iexact=category_name)

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(self.get_serializer(products, many=True).data)

    @action(detail=False, methods=['get'])
    def available(self, request):
        """
        Returns all products that:
        - Are marked as available
        - Have stock greater than 0
        """
        products = self.get_queryset().filter(
            is_available=True,
            stock_quantity__gt=0
        )

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(self.get_serializer(products, many=True).data)
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """
        Returns all reviews for a specific product.
        GET /api/products/{id}/reviews/
        """
        product = self.get_object()
        reviews = product.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_review(self, request, pk=None):
        """
        Allows an authenticated user to submit a review for a product.
        POST /api/products/{id}/add_review/
        """
        product = self.get_object()

        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create review linked to user and product
        Review.objects.create(
            product=product,
            user=request.user,
            rating=serializer.validated_data['rating'],
            comment=serializer.validated_data.get('comment', '')
        )

        return Response(
            {"message": "Review added successfully"},
            status=status.HTTP_201_CREATED
        )

