from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Product model creation and attributes
class Product(models.Model):
    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=250, blank=True)
    long_description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='fitshop_products/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
# Cart item functionality
class CartItem(models.Model):

    # Guests cannot use the cart 
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    # The specific product the user added to their cart.
    product = models.ForeignKey(
        'fitshop.Product',
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    # How many units of this product the user wants.
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        # Example: “Dumbell set x 2”
        return f"{self.product.name} x {self.quantity}"

    @property
    def subtotal(self):
        # Price for this cart line: product price × quantity.
        return self.product.price * self.quantity