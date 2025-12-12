from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Cart(models.Model):
    """
    A shopping cart belongs to a single user.
    Each user has one active cart at a time.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"

    @property
    def total_items(self):
        return self.items.count()

    @property
    def total_price(self):
        """
        Calculates total price of all items in cart.
        """
        return sum(item.subtotal for item in self.items.all())


class CartItem(models.Model):
    """
    Represents one product inside a cart.
    quantity indicates how many units of the product are in the cart.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')  # Prevent duplicate items

    @property
    def subtotal(self):
        """
        Price of this item (product price × quantity).
        """
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"
