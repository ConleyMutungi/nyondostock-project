from django.db import models

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name
    
# class Order(models.Model):
#     id = models.ForeignKey('id', on_delete=models.CASCADE)
#     Product_Relationship = models.ForeignKey('Product', on_delete=models.CASCADE)
#     Quantity = models.IntegerField()
#     Amount = models.DecimalField(max_digits=20, decimal_places=2)
#     Customer_Relationship = models.ForeignKey('Customer', on_delete=models.SET_NULL)
#     Method = models.CharField(max_length=255)
#     date = models.DateTimeField(auto_now_add=True)
#     Recorded_by = models.ForeignKey('User', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name
    