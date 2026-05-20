from django.db import models

# Create your models here.
class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity_sold = models.IntegerField()
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

   

class Expense(models.Model):
    description = models.CharField(max_length=225)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

# class Payments(models.Model):
#     id = models.ForeignKey('id', on_delete=models.CASCADE)
#     Order_Relationship = models.ForeignKey('Order', on_delete=models.CASCADE)
#     Customer_Relationship = models.ForeignKey('Customer', on_delete=models.CASCADE)
#     Amount = models.DecimalField(max_digits=20, decimal_places=2)
#     Balance = models.DecimalField(max_digits=20, decimal_places=2)
#     Comments = models.TextField(blank=True) #May change this in future
#     Recorded_By = models.ForeignKey('User', on_delete=models.SET_NULL)

#     def __str__(self):
#         return self.name