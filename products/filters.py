import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    """
    This class defines advanced filtering logic for Product queries.
    Django Filter automatically reads the URL query parameters and
    applies corresponding filters to the queryset.

    Example usage from frontend or Postman:
      /api/products/?name=rice
      /api/products/?category=Electronics
      /api/products/?min_price=100&max_price=500
      /api/products/?in_stock=true
    """

    # Filter products where name contains a given substring
    # lookup_expr='icontains' means: case-insensitive partial match
    name = django_filters.CharFilter(lookup_expr='icontains')

    # Allows filtering by category name, not category ID
    # e.g. /api/products/?category=Fruits
    category = django_filters.CharFilter(
        field_name='category__name',  # Follow the FK: Product.category.name
        lookup_expr='iexact'          # Exact match, but ignore case
    )

    # Minimum price filter (price >= min_price)
    min_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte'  # greater than or equal
    )

    # Maximum price filter (price <= max_price)
    max_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte'  # less than or equal
    )

    # Boolean filter for checking stock availability
    # Calls custom method filter_in_stock()
    in_stock = django_filters.BooleanFilter(method='filter_in_stock')



    class Meta:
        """
        Meta tells Django Filter which model to apply filtering to
        and which fields are allowed to be filtered.
        """
        model = Product

        # These fields allow direct filtering:
        # - category (via FK)
        # - is_available (boolean)
        fields = ['category', 'is_available']



    def filter_in_stock(self, queryset, name, value):
        """
        Custom filter function.

        Called when user passes:
            /api/products/?in_stock=true
        or:
            /api/products/?in_stock=false

        value = True → return products with stock_quantity > 0  
        value = False → return products with stock_quantity == 0  
        """
        if value:
            return queryset.filter(stock_quantity__gt=0)
        return queryset.filter(stock_quantity=0)
