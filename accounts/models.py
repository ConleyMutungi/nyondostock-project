from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
ROLE_CHOICES = [
    ('customer', 'Customer'),
    ('sales_attendant', 'Sales Attendant'),
    ('store_manager', 'Store Manager'),
    ('accounts_admin', 'Accounts Admin'),
]

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    is_staff_member = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_sales_attendant(self):
        return self.role == 'sales_attendant'

    @property
    def is_store_manager(self):
        return self.role == 'store_manager'

    @property
    def is_accounts_admin(self):
        return self.role == 'accounts_admin'
    
# class Customer(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)
#     contact_info = models.CharField(max_length=255)
#     email = models.EmailField()

#     def __str__(self):
#         return self.name

class Staff(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='staff_profile')
    profile_picture = models.ImageField(upload_to='staff_profiles/', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    contact_info = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.user.username
