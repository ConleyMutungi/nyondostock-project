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


class Payments(models.Model):
    id = models.ForeignKey('id', on_delete=models.CASCADE)
    Order_Relationship = models.ForeignKey('Order', on_delete=models.CASCADE)
    Customer_Relationship = models.ForeignKey('Customer', on_delete=models.CASCADE)
    Amount = models.DecimalField(max_digits=20, decimal_places=2)
    Balance = models.DecimalField(max_digits=20, decimal_places=2)
    Comments = models.TextField(blank=True) #May change this in future
    Recorded_By = models.ForeignKey('User', on_delete=models.SET_NULL)

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
    
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name
    
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

class User(models.AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(min_length=8)

def __str__(self):
        return self.username

class Expense(models.Model):
    description = models.CharField(max_length=225)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity_sold = models.IntegerField()
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    #ai recommended I add Project Business Pages from Customers
    class StaffDashboardView(UserPassesTestMixin, ListView):
        model = Sale
        template_name = 'finance/dashboard.html'   #Check this and research it

    #This test determines whether the user is allowed on this page
    def test_func(self):
        return self.request.user_is.authenticated and self.request.user.is_staf_member

# @login_required
# def financial_dashboard(request):
#     #Sum up all sales revenue
#     total_sales = Sale.objects.aggregate(Sum('total_revenue'))['total_revenue_sum'] or 0

#     #Sum up all business expenses
#     total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    
#     #Calculate final net profit using standard math: Profit = Revenue - Expenses
#     net_profit = total_sales - total_expenses