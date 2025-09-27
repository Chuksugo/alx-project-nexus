# payments/models.py
import uuid
from django.db import models
from django.conf import settings
from orders.models import Order


class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]

    METHOD_CHOICES = [
        ("paystack", "Paystack"),
        ("card", "Card"),
        ("bank_transfer", "Bank Transfer"),
    ]

    email = models.EmailField()
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="payment"
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(
        max_length=100, unique=True, default=uuid.uuid4, editable=False
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    payment_method = models.CharField(
        max_length=20, choices=METHOD_CHOICES, default="paystack"
    )
    access_code = models.CharField(max_length=200, blank=True, null=True)
    transaction_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Ensure reference is always set
        if not self.reference:
            self.reference = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment({self.reference}) - {self.customer} - {self.status}"
