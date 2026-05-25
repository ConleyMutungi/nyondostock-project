from django.shortcuts import redirect, render
from django.db.models import Sum

from stock.models import Stock
from .models import Sale, Expense, CustomerProfile, CreditTransaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .models import CustomerProfile, CreditTransaction
from django.contrib.auth.decorators import login_required
from nyondo.finance.models import CustomerProfile
from .forms import SaleForm


# Create your views here.
@login_required
def financial_dashboard(request):
    #Sum up all sales revenue
    total_sales = Sale.objects.aggregate(Sum('total_revenue'))['total_revenue_sum'] or 0

    #Sum up all business expenses
    total_expenses = Expense.objects.aggregate(Sum('price'))['price__sum'] or 0
    
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


def process_credit_purchase(user, total_cost, order_details=""):
    # Ensure database integrity
    with transaction.atomic():
        # select_for_update() locks the row until the transaction finishes
        # This prevents the user from double-clicking and spending credit twice simultaneously
        profile = CustomerProfile.objects.select_for_update().get(user=user)
        
        if profile.credit_balance < total_cost:
            raise ValidationError("Insufficient store credit to complete this purchase.")
        
        # Deduct the cost
        profile.credit_balance -= total_cost
        profile.save()
        
        #   The history jazz of everything 
        CreditTransaction.objects.create(
            profile=profile,
            amount=total_cost,
            transaction_type='PURCHASE',
            description=order_details
        )

def reload_customer_credit(user, deposit_amount, reference=""):
    with transaction.atomic():
        profile = CustomerProfile.objects.select_for_update().get(user=user)
        
        profile.credit_balance += deposit_amount
        profile.save()
        
        CreditTransaction.objects.create(
            profile=profile,
            amount=deposit_amount,
            transaction_type='RELOAD',
            description=f"Deposit made. Ref: {reference}"
        )

#@login_required
def credit_dashboard(request):
    # Automatically creates a profile if it doesn't exist yet (signals can also do this)
    profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    
    # Get the history, newest first
    transactions = profile.transactions.all().order_by('-created_at')
    
    context = {
        'profile': profile,
        'transactions': transactions
    }
    return render(request, 'store/credit_dashboard.html', context)


def sales_reg_form(request):
    if request.method == 'POST':
        # name = request.POST.get('web_name')
        form = SaleForm(request.POST)
        if form.is_valid():
            stock = form.cleaned_data['stock']
            if stock.quantity < form.cleaned_data['quantity_sold']:
                form.add_error('quantity_sold', 'Not enough stock available.')
            else:
                form.save()
                return redirect('sales_reg_form')
            if  stock.quantity >= quantity_sold:
                stock.quantity -= models.F('quantity') - quantity_sold #or quantity_sold
                stock.save()
    else:
        form = SaleForm()
    context = {
        'form' : form
    }
    return render(request, 'sales_reg_form.html', {'form':form})

@login_required
def sales_list(request):
    sales = Sale.objects.all()
    return render (request, 'sales_list.html', {'sales':sales})