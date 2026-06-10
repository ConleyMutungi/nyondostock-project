from django.contrib import admin
from .models import Delivery, Expense, Sale


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
	list_display = ('sale', 'distance', 'fee', 'status', 'created_at')


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
	list_display = ('id', 'stock', 'quantity_sold', 'delivery_distance', 'delivery_fee', 'date')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
	list_display = ('id', 'stock', 'price', 'transport_cost', 'tax_amount', 'total_amount', 'date')
