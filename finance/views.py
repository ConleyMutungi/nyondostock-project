from django.shortcuts import render
from django.db.models import Sum
from .models import Sale, Expense
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView

# Create your views here.
# @login_required
def financial_dashboard(request):
    #Sum up all sales revenue
    total_sales = Sale.objects.aggregate(Sum('total_revenue'))['total_revenue_sum'] or 0

    #Sum up all business expenses
    total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    
    #Calculate final net profit using standard math: Profit = Revenue - Expenses
    net_profit = total_sales - total_expenses

    context = {
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
    }
    return render(request, 'finance/dashboard.html', context) # First create dashboard.html

        #ai recommended I add Project Business Pages from Customers
    class StaffDashboardView(UserPassesTestMixin, ListView):
        model = Sale
        template_name = 'finance/dashboard.html'   #Check this and research it

    #This test determines whether the user is allowed on this page
    def test_func(self):
        return self.request.user_is.authenticated and self.request.user.is_staf_member