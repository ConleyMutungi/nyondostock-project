from django.db import models

# Create your models here.

class CustomUser(models.AbstractUser):
    # id = models.AutoField(primary_key=True)
    # username = models.CharField(max_length=255)
    # email = models.EmailField()
    # password = models.CharField(min_length=8)
    is_customer = models.BooleanField(default=True)
    is_staff_member = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name    

class Staff(models.AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(min_length=8)

def __str__(self):
        return self.username
