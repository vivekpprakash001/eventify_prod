from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class RazorpayTransaction(models.Model):
    # Optional: who this transaction relates to
    user = models.ForeignKey(User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="razorpay_transactions",
    )

    # Razorpay identifiers
    razorpay_order_id = models.CharField(max_length=191, unique=True)
    razorpay_payment_id = models.CharField(max_length=191, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)

    # Generic linkage to any domain object (order, booking, wallet topup, etc.)
    reference_type = models.CharField(
        max_length=100,
        blank=True, null=True,
        help_text="What this payment is for, e.g. 'booking', 'wallet_topup', 'ticket'",
    )
    transaction_id = models.CharField(
        max_length=100,
        blank=True, null=True,
        help_text="ID of the related for the transaction",
    )

    # Amount info (Razorpay uses smallest unit, e.g. paise)
    amount = models.BigIntegerField(help_text="Amount in paise")
    currency = models.CharField(max_length=10, default="INR")

    # Status & method
    status = models.CharField(
        max_length=50,
        help_text="created/authorized/captured/failed/refunded",
    )
    method = models.CharField(
        max_length=50,
        blank=True, null=True,
        help_text="card/netbanking/wallet/upi/etc",
    )
    email = models.EmailField(blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)

    # Errors
    error_code = models.CharField(max_length=100, blank=True, null=True)
    error_description = models.TextField(blank=True, null=True)

    # Extra data
    notes = models.JSONField(blank=True, null=True)
    raw_gateway_response = models.JSONField(
        blank=True, null=True,
        help_text="Full payload from Razorpay",
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    captured_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.razorpay_payment_id or self.razorpay_order_id} - {self.status}"

    def __save__(self):
        if not self.transaction_id: 
            self.transaction_id = str(uuid.uuid4().hex[:10]).upper()
        super().save(*args, **kwargs)
