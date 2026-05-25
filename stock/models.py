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
     
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, choices=STOCK_CHOICES)
    # symbol = models.CharField(max_length=255)
    # Product_Relationship = models.ForeignKey('Product', on_delete=models.CASCADE)
    Supplier_Relationship = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    # Customer_Relationship = models.ForeignKey('Customer', on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    Date = models.DateTimeField(auto_now_add=True)
    Total_Cost = models.DecimalField(max_digits=20, decimal_places=2)
    is_on_credit = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    low_stock_threshold = models.IntegerField(default=5)
    # image = models.ImageField(upload_to='stock/')

    def __str__(self):
        return f"{self.product.name} - {self.quantity} items left"
    
class Supplier(models.Model):
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    Address = models.CharField(max_length=25)
    email = models.EmailField()
    nin = models.CharField(max_length=14)
    stock_supplied = models.ForeignKey('Stock', on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

# class Product(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     price = models.DecimalField(max_digits=20, decimal_places=2)
#     image = models.ImageField(upload_to='products/')

#     def __str__(self):
#         return self.name



    





 