from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.core.validators import MinValueValidator


class Order(models.Model):
    """
    Represents a placed order by a user.
    Contains multiple OrderItems and a final total cost.
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    @property
    def total_items(self):
        return self.items.count()

    def calculate_total(self):
        """
        Recalculate order total from its items.
        """
        total = sum(item.subtotal for item in self.items.all())
        self.total_price = total
        self.save()
        return total


class OrderItem(models.Model):
    """
    A single item inside an order.
    Captures price at the time of purchase.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        """
        Price at the time of purchase × quantity.
        """
        return self.price_at_purchase * self.quantity

    def __str__(self):
        return f"{self.quantity} × {self.product}"
