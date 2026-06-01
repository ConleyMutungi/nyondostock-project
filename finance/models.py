from django.db import models
# from stock.models import Supplier
from accounts.models import Staff
from stock.models import Stock
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone
from stock.models import Stock

# Create your models here.
class Sale(models.Model):
    staff = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sales',
        db_column='customer_id'
    )
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    stock = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True)
    quantity_sold = models.IntegerField()
    # total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Recorded_By = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    # supplied_by = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        stock_name = self.stock.name if self.stock else 'Unknown'
        return f"Sale: {stock_name} - {self.quantity_sold}"

    def save(self, *args, **kwargs):
        if self.stock is not None:
            self.unit_price = self.stock.unit_price
        super().save(*args, **kwargs)

    @property
    def total_revenue(self):
        return (self.unit_price or Decimal('0.00')) * Decimal(self.quantity_sold or 0)

class Expense(models.Model):
    price = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    transport_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    Comments = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    # Recorded_By = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    # Supplier_Relationship = models.ForeignKey('stock.Supplier', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.transport_cost = abs(self.transport_cost or Decimal('0.00'))
        self.tax_amount = abs(self.tax_amount or Decimal('0.00'))
        self.price = abs(self.price or Decimal('0.00'))
        self.total_amount = self.price + self.transport_cost + self.tax_amount
        super().save(*args, **kwargs)

class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    # forcing in DecimalField for finance data to avoid float errors apparently
    credit_balance = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))] # Prevents debt if you only want prepaid store credit
    )

    def __str__(self):
        return f"{self.user.username} - Balance: ${self.credit_balance}"

class CreditTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('RELOAD', 'Account Reload/Payment'),
        ('PURCHASE', 'Store Purchase'),
        ('REFUND', 'Return Refund'),
    ]

    profile = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2) # Always positive
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.TextField(blank=True, help_text="e.g., Purchased 10x Bags of Cement")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} by {self.profile.user.username}"

class PendingCreditOrder(models.Model):
    profile = models.ForeignKey('CustomerProfile', on_delete=models.CASCADE, related_name='pending_orders')
    stock = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    total_cost = models.DecimalField(max_digits=20, decimal_places=2)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user = self.profile.user.username if self.profile and self.profile.user else 'Unknown'
        stock_name = self.stock.name if self.stock else 'Unknown'
        return f"PendingOrder: {user} -> {stock_name} x{self.quantity} ({self.total_cost})"