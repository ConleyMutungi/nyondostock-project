from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.financial_dashboard, name='financial_dashboard'),
    path('staff-dashboard/', views.StaffDashboardView.as_view(), name='staff_dashboard'),
    path('process-credit-purchase/', views.process_credit_purchase, name='process_credit_purchase'),
    path('sales/new/', views.credit_dashboard, name='create_sale'),
    path('sales/', views.sales_list, name='sales_list'),
    path('expenses/new/', views.sales_reg_form, name='create_expense'),
    path('reload-credit/', views.reload_customer_credit, name='reload_credit'),
]