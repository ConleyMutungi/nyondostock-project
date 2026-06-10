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
    delivery_distance = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    delivery_fee = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    date = models.DateField(auto_now_add=True)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    expense_amount = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    net_profit = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    # Recorded_By = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    # supplied_by = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        stock_name = self.stock.name if self.stock else 'Unknown'
        return f"Sale: {stock_name} - {self.quantity_sold}"

    def save(self, *args, **kwargs):
        if self.stock is not None:
            self.unit_price = self.stock.unit_price
        self.delivery_fee = self.calculate_delivery_fee(self.delivery_distance)
        # Calculate expenses and net profit per sale
        total_revenue = (self.unit_price or Decimal('0.00')) * Decimal(self.quantity_sold or 0)
        cost_of_goods = (self.stock.unit_cost if self.stock and self.stock.unit_cost is not None else Decimal('0.00')) * Decimal(self.quantity_sold or 0)
        pct = getattr(settings, 'SALE_EXPENSE_PERCENTAGE', Decimal('0.10'))
        try:
            pct = Decimal(pct)
        except Exception:
            pct = Decimal('0.10')
        self.expense_amount = (total_revenue * pct).quantize(Decimal('0.01'))
        # Net profit = revenue - COGS - expense - delivery fee
        self.net_profit = (total_revenue - cost_of_goods - self.expense_amount - (self.delivery_fee or Decimal('0.00'))).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)

    @staticmethod
    def calculate_delivery_fee(distance):
        try:
            distance = float(distance or 0)
        except (TypeError, ValueError):
            return Decimal('0.00')

        if distance <= 2:
            return Decimal('0.00')
        if distance <= 8:
            return Decimal('5000.00')
        if distance <= 18:
            return Decimal('10000.00')
        if distance <= 25:
            return Decimal('15000.00')
        return Decimal('30000.00')

    @property
    def total_revenue(self):
        return (self.unit_price or Decimal('0.00')) * Decimal(self.quantity_sold or 0)

    @property
    def total_amount_due(self):
        return self.total_revenue + (self.delivery_fee or Decimal('0.00'))

class Expense(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True, blank=True)
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
        if self.stock is not None:
            self.price = self.stock.unit_cost or Decimal('0.00')
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


class Delivery(models.Model):
    sale = models.OneToOneField('Sale', on_delete=models.CASCADE, related_name='delivery')
    distance = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))
    fee = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SCHEDULED', 'Scheduled'),
        ('DELIVERED', 'Delivered'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        sale_id = self.sale.pk if self.sale else 'N/A'
        return f"Delivery for Sale #{sale_id} - {self.status}"
