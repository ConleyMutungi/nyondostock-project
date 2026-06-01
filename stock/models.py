from decimal import Decimal
from django.db import models
from django.utils import timezone

# Create your models here.

class StockManager(models.Manager):
    # """Custom manager to automatically filter out soft-deleted items."""
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
    
class Stock(models.Model):
    STOCK_CHOICES = [
      ('hammers', 'Hammers'),
      ('nails', 'Nails'),
      ('iron sheets', 'Iron Sheets'),
      ('cement', 'Cement'),
      ('toolbox','Toolbox'),
      ('timber', 'Timber'),
      ('wire mesh', 'Wire Mesh'),
    ]
     
    name = models.CharField(max_length=25, choices=STOCK_CHOICES)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    unit_cost = models.DecimalField(max_digits=20, decimal_places=2)
    total_cost = models.DecimalField(max_digits=20, decimal_places=2)
    is_on_credit = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    low_stock_threshold = models.IntegerField(default=5)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    
    # Managers
    objects = StockManager()  # Default manager - excludes deleted
    all_objects = models.Manager()  # Get all, including deleted
    
    def save(self, *args, **kwargs):
        if self.unit_cost is None:
            self.unit_cost = Decimal('0.00')
        if self.quantity is None:
            self.quantity = 0

        self.total_cost = self.quantity * self.unit_cost

        # if self.quantity <= 0:
        #     self.is_deleted = True
        #     self.deleted_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.quantity} left)"

    @property
    def potential_revenue(self):
        return (self.unit_price or Decimal('0.00')) * Decimal(self.quantity or 0)

    # image = models.ImageField(upload_to='stock/')

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    Address = models.CharField(max_length=25)
    email = models.EmailField()
    nin = models.CharField(max_length=14)
    stock_supplied = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True)
    

    def __str__(self):
        return self.name



 