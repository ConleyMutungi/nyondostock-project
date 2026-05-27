from django.db import models

# Create your models here.

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
    total_cost = models.DecimalField(max_digits=20, decimal_places=2)
    is_on_credit = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    low_stock_threshold = models.IntegerField(default=5)
    # image = models.ImageField(upload_to='stock/')

    def __str__(self):
      return f"{self.name} - {self.quantity} items left"
    
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    Address = models.CharField(max_length=25)
    email = models.EmailField()
    nin = models.CharField(max_length=14)
    stock_supplied = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name



 