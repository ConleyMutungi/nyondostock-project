from django.db import models
# from nyondo.stock.models import Supplier
# from nyondo.accounts.models import Staff
# from nyondo.stock.models import Product
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.
class Sale(models.Model):
    stock = models.ForeignKey('Stock', on_delete=models.SET_NULL, null=True)
    quantity_sold = models.IntegerField()
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Sale: {self.stock.name} - {self.quantity_sold}"

# class Expense(models.Model):
#     description = models.CharField(max_length=225)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     

class Expense(models.Model):
    #Order_Relationship = models.ForeignKey('Order', on_delete=models.CASCADE)
    Supplier_Relationship = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    # Product_Relationship = models.ForeignKey('Product', on_delete=models.CASCADE)
    #Customer_Relationship = models.ForeignKey('Customer', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    Balance = models.DecimalField(max_digits=20, decimal_places=2)
    Comments = models.TextField(blank=True) #May change this in future
    Recorded_By = models.ForeignKey('Staff', on_delete=models.SET_NULL)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
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