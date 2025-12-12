from django.db import models

class Category(models.Model):
    """
    Represents a product category in the store.
    Examples: Electronics, Fruits, Clothing, Beverages.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # When category was added
    updated_at = models.DateTimeField(auto_now=True)      # Updated anytime admin edits

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']  # Alphabetical order

    def __str__(self):
        return self.name

    @property
    def product_count(self):
        """
        Returns how many products belong to this category.
        Used to show category stats without extra work.
        """
        return self.products.count()
