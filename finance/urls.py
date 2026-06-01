from django.urls import path
from . import views

urlpatterns = [
    path('financial-dashboard/', views.financial_dashboard, name='dashboard'),
    path('register/', views.financial_dashboard, name='financial_dashboard'),
    path('staff-dashboard/', views.StaffDashboardView.as_view(), name='staff_dashboard'),
    path('process-credit-purchase/', views.process_credit_purchase, name='process_credit_purchase'),
    path('credit-dashboard/', views.credit_dashboard, name='credit_dashboard'),
    path('expenses/new/', views.expense_reg_form, name='expense_registration_form'),
    path('', views.sales_list, name='sales_list'),
    path('sales/new/', views.sales_reg_form, name='sales_reg_form'),
    path('reload-credit/', views.deposit_customer_credit, name='reload_credit'),
    path('receipt/<int:pk>/', views.generate_receipt, name='generate_receipt'),
]