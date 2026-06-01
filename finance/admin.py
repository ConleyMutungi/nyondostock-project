from django.contrib import admin
from .models import Delivery, Sale


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
	list_display = ('sale', 'distance', 'fee', 'status', 'created_at')


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
	list_display = ('id', 'stock', 'quantity_sold', 'delivery_distance', 'delivery_fee', 'date')
