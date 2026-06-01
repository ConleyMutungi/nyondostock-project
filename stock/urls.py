from django.urls import path
from . import views

urlpatterns = [
    path('supplierform/', views.supplier_reg_form, name='supplier_registration_form'),
    path('supplierlist/', views.supplier_list, name='supplier_list'),
    path('supplierlist/delete/<int:pk>/', views.delete_supplier, name='delete_supplier'),
    path('supplier/<int:pk>/', views.supplier_detail, name='supplier_detail'),
    path('stockform/', views.stock_reg_form, name='stock_registration_form'),
    path('stocklist/', views.stock_list, name='stock_list'),
    path('stock/detail/<int:pk>/', views.stock_detail, name='stock_detail'),
    path('stock/edit/<int:pk>/', views.stock_edit, name='stock_edit'),
    path('stock/restock/<int:pk>/', views.stock_restock, name='stock_restock'),
    path('stocklist/delete/<int:pk>/', views.stock_delete, name='stock_delete'),
]