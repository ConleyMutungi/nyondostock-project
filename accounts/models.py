from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    # is_customer = models.BooleanField(default=True)
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

class Staff(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='staff_profile')
    profile_picture = models.ImageField(upload_to='staff_profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username
