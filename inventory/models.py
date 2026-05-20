from django.db import models

# Create your models here.

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    # symbol = models.CharField(max_length=255)
    Product_Relationship = models.ForeignKey('Product', on_delete=models.CASCADE)
    Supplier_Relationship = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    User_Relationship = models.ForeignKey('User', on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    Date = models.DateTimeField(auto_now_add=True)
    Total_Cost = models.DecimalField(max_digits=20, decimal_places=2)
    is_on_credit = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    low_stock_threshold = models.IntegerField(default=5)

    def __str__(self):
        return f"{sef.product.name} - {self.quantity} items left"
    
class Supplier(models.Model):
    id = models.ForeignKey('id', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    Address = models.CharField(max_length=25)
    email = models.EmailField()


    def __str__(self):
        return self.name




    





 