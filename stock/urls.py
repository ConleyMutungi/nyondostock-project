from django.urls import path
from . import views
from .views import delete_supplier


urlpatterns = [
    path('supplierform/',views.supplier_reg_form, name='supplier_registration_form'),
    path('supplierlist/',views.supplier_list, name='supplier_list'),
    path('stockform/',views.stock_reg_form, name='stock_registration_form'),
    path('stocklist/',views.stock_list, name='stock_list'),
    path('supplierlist/delete/<int:pk>/', delete_supplier, name='delete_supplier')
]