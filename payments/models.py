from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SubscriptionTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscription_transactions')
    amount = models.DecimalField(max_digits=6, decimal_places=2, help_text="Amount paid for the subscription")
    
    # Order ID from PayPal/Stripe
    order_id = models.CharField(max_length=100, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sub {self.order_id} - {self.user.username}"
