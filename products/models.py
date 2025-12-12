from django.db import models
from django.contrib.auth.models import User
from categories.models import Category
from django.core.validators import MinValueValidator

class Product(models.Model):
    """
    Represents a single product in the e-commerce store.
    Includes price, images, category, stock tracking and creator info.
    """

    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]  # Price must be > 0
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,  # Delete products if category is removed
        related_name="products"
    )

    stock_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    # URL-based images
    image_url = models.URLField(max_length=500, blank=True)

    # Actual uploaded image
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_date = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Keep product when user deleted
        null=True,
        related_name='products'
    )

    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_date']  # Newest first
        indexes = [
            models.Index(fields=['name', 'category']),
            models.Index(fields=['price']),
        ]

    def __str__(self):
        return self.name

    @property
    def in_stock(self):
        """
        True if stock quantity > 0
        """
        return self.stock_quantity > 0
