from decimal import Decimal, InvalidOperation
import json

from django.shortcuts import redirect, render
from django.db.models import Q, Sum, F, Value, ExpressionWrapper, DecimalField, Max
from django.db.models.functions import Coalesce
from stock.models import Stock
from .models import Sale, CustomerProfile, CreditTransaction, Expense, PendingCreditOrder, Delivery
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .forms import SaleForm, ExpenseForm
from django.contrib import messages
from django.views.decorators.http import require_POST

CURRENCY_CODE = 'UGX'


def get_credit_profile(user):
    return getattr(user, 'profile', None)


# Create your views here.
@login_required
def financial_dashboard(request):
    revenue_expression = ExpressionWrapper(
        F('quantity_sold') * Coalesce(F('unit_price'), Value(0)),
        output_field=DecimalField(max_digits=20, decimal_places=2)
    )
    total_sales = Sale.objects.aggregate(total_revenue=Sum(revenue_expression))['total_revenue'] or Decimal('0.00')
    expense_totals = Expense.objects.aggregate(
        total_price=Sum('price'),
        total_transport=Sum('transport_cost'),
        total_tax=Sum('tax_amount'),
    )
    total_expenses = (
        (expense_totals['total_price'] or Decimal('0.00'))
        + (expense_totals['total_transport'] or Decimal('0.00'))
        + (expense_totals['total_tax'] or Decimal('0.00'))
    )
    net_profit = total_sales - total_expenses
    context = {
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
    }
    return render(request, 'includes/dashboard.html', context)


class StaffDashboardView(UserPassesTestMixin, ListView):
    model = Sale
    template_name = 'includes/dashboard.html'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in ['sales_attendant', 'store_manager', 'accounts_admin']


@login_required
def process_credit_purchase(request):
    if request.method != 'POST':
        return redirect('credit_dashboard')

    profile = get_credit_profile(request.user)
    if profile is None:
        return redirect('join_credit_scheme')

    try:
        stock_id = int(request.POST.get('stock_id'))
        quantity = int(request.POST.get('quantity', '1'))
    except (TypeError, ValueError):
        return redirect('stock_list')

    stock = get_object_or_404(Stock, pk=stock_id)
    total_cost = (stock.unit_price or Decimal('0.00')) * Decimal(quantity)

    with transaction.atomic():
        profile = CustomerProfile.objects.select_for_update().get(pk=profile.pk)

        if profile.credit_balance >= total_cost:
            # Complete purchase immediately
            profile.credit_balance -= total_cost
            profile.save()

            # create sale record
            Sale.objects.create(
                stock=stock,
                quantity_sold=quantity,
                unit_price=stock.unit_price,
            )

            # update stock
            if stock.quantity is None:
                stock.quantity = 0
            stock.quantity = max(0, stock.quantity - quantity)
            stock.save()

            CreditTransaction.objects.create(
                profile=profile,
                amount=total_cost,
                transaction_type='PURCHASE',
                description=f"Purchase of {stock.name} x{quantity}"
            )
        else:
            # Create a pending order so user can deposit increments
            PendingCreditOrder = __import__('finance.models', fromlist=['PendingCreditOrder']).PendingCreditOrder
            PendingCreditOrder.objects.create(
                profile=profile,
                stock=stock,
                quantity=quantity,
                total_cost=total_cost
            )

    return redirect('credit_dashboard')


@login_required
def deposit_customer_credit(request):
    if request.method != 'POST':
        return redirect('credit_dashboard')

    profile = get_credit_profile(request.user)
    if profile is None:
        return redirect('join_credit_scheme')

    try:
        deposit_amount = Decimal(request.POST.get('deposit_amount', '0.00'))
    except InvalidOperation:
        return redirect('credit_dashboard')

    reference = request.POST.get('reference', '')

    if deposit_amount <= 0:
        return redirect('credit_dashboard')

    with transaction.atomic():
        profile = CustomerProfile.objects.select_for_update().get(pk=profile.pk)
        profile.credit_balance += deposit_amount
        profile.save()

        CreditTransaction.objects.create(
            profile=profile,
            amount=deposit_amount,
            transaction_type='RELOAD',
            description=f"Deposit made. Ref: {reference}"
        )

        # After deposit, check for pending orders and fulfill any that can be paid for now.
        pending = PendingCreditOrder.objects.filter(profile=profile, is_completed=False).order_by('created_at')
        for order in pending:
            # reload profile from DB to get updated balance
            profile.refresh_from_db()
            stock = order.stock
            if not stock:
                continue
            # ensure enough balance and stock quantity
            if profile.credit_balance >= order.total_cost and (stock.quantity or 0) >= order.quantity:
                # Deduct balance
                profile.credit_balance -= order.total_cost
                profile.save()

                # Create Sale
                Sale.objects.create(
                    stock=stock,
                    quantity_sold=order.quantity,
                    unit_price=stock.unit_price,
                )

                # Update stock
                stock.quantity = max(0, stock.quantity - order.quantity)
                stock.save()

                # Mark order completed
                order.is_completed = True
                order.save()

                # Record transaction
                CreditTransaction.objects.create(
                    profile=profile,
                    amount=order.total_cost,
                    transaction_type='PURCHASE',
                    description=f"Auto-completed pending purchase of {stock.name} x{order.quantity}"
                )

    return redirect('credit_dashboard')


@login_required
def join_credit_scheme(request):
    profile = get_credit_profile(request.user)
    if profile is not None:
        return redirect('credit_dashboard')

    if request.method == 'POST':
        profile = CustomerProfile.objects.create(user=request.user)
        return redirect('credit_dashboard')

    return render(request, 'store/join_credit.html')


@login_required
def credit_dashboard(request):
    profile = get_credit_profile(request.user)
    transactions = []
    pending_orders = []
    totals = {
        'total_reloads': 0,
        'total_purchases': 0,
        'total_refunds': 0,
    }

    if profile is not None:
        transactions = profile.transactions.all().order_by('-created_at')
        pending_orders = profile.pending_orders.filter(is_completed=False).order_by('-created_at')
        totals = profile.transactions.aggregate(
            total_reloads=Sum('amount', filter=Q(transaction_type='RELOAD')),
            total_purchases=Sum('amount', filter=Q(transaction_type='PURCHASE')),
            total_refunds=Sum('amount', filter=Q(transaction_type='REFUND')),
        )

    context = {
        'profile': profile,
        'transactions': transactions,
        'pending_orders': pending_orders,
        'current_balance': profile.credit_balance if profile else Decimal('0.00'),
        'total_reloads': totals['total_reloads'] or 0,
        'total_purchases': totals['total_purchases'] or 0,
        'total_refunds': totals['total_refunds'] or 0,
        'currency_code': CURRENCY_CODE,
    }
    return render(request, 'store/credit_dashboard.html', context)


@login_required
def expense_reg_form(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense recorded successfully!')
            return redirect('expenses_list')
    else:
        form = ExpenseForm()

    stock_purchase_prices = {
        str(stock.pk): str(stock.unit_cost or Decimal('0.00'))
        for stock in Stock.objects.only('pk', 'unit_cost')
    }

    return render(request, 'store/expense_reg_form.html', {
        'form': form,
        'stock_purchase_prices': json.dumps(stock_purchase_prices),
    })


@login_required
def expenses_list(request):
    """Display all recorded expenses with filtering and pagination"""
    expenses = Expense.objects.select_related('stock').order_by('-date')
    
    # Optional filtering by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if date_from:
        try:
            from django.utils.dateparse import parse_date
            expenses = expenses.filter(date__gte=parse_date(date_from))
        except Exception:
            pass
    
    if date_to:
        try:
            from django.utils.dateparse import parse_date
            expenses = expenses.filter(date__lte=parse_date(date_to))
        except Exception:
            pass
    
    # Calculate totals
    expense_summary = expenses.aggregate(
        total_price=Sum('price'),
        total_transport=Sum('transport_cost'),
        total_tax=Sum('tax_amount'),
        total_amount=Sum('total_amount'),
    )
    
    context = {
        'expenses': expenses,
        'expense_summary': expense_summary,
        'currency_code': CURRENCY_CODE,
    }
    
    return render(request, 'store/expenses_list.html', context)


@login_required
def credit_members_list(request):
    if request.user.role not in ['store_manager', 'accounts_admin']:
        return redirect('dashboard')

    profiles = CustomerProfile.objects.select_related('user').order_by('-credit_balance')
    return render(request, 'store/credit_members.html', {'profiles': profiles, 'currency_code': CURRENCY_CODE})


def sales_reg_form(request):
    selected_stock = None
    initial = {}

    stock_id = request.GET.get('stock')
    if stock_id:
        try:
            selected_stock = Stock.objects.get(pk=int(stock_id))
            initial['stock'] = selected_stock
        except (Stock.DoesNotExist, ValueError):
            selected_stock = None

    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            quantity_sold = form.cleaned_data['quantity_sold']
            stock = form.cleaned_data['stock']
            if stock.quantity < quantity_sold:
                form.add_error('quantity_sold', 'Not enough stock available.')
            else:
                sale = form.save(commit=False)
                sale.staff = getattr(request.user, 'staff_profile', None)
                sale.unit_price = stock.unit_price or Decimal('0.00')
                sale.save()
                # create a delivery record if distance provided
                try:
                    if (sale.delivery_distance or Decimal('0.00')) > Decimal('0.00'):
                        # avoid duplicate deliveries
                        if not hasattr(sale, 'delivery'):
                            Delivery.objects.create(
                                sale=sale,
                                distance=sale.delivery_distance,
                                fee=sale.delivery_fee,
                                status='PENDING'
                            )
                except Exception:
                    # Don't block sale creation on delivery record errors
                    pass
                stock.quantity -= quantity_sold
                stock.save()
                return redirect('sales_list')
    else:
        form = SaleForm(initial=initial)

    return render(request, 'store/sales_reg_form.html', {
        'form': form,
        'selected_stock': selected_stock,
    })

@login_required
def sales_list(request):
    sales = Sale.objects.all()
    return render(request, 'store/sales_list.html', {'sales':sales})

@login_required
def sales_by_stock_report(request):
    revenue_expression = ExpressionWrapper(
        F('quantity_sold') * Coalesce(F('unit_price'), Value(0)),
        output_field=DecimalField(max_digits=20, decimal_places=2)
    )
    report = (
        Sale.objects
            .filter(stock__isnull=False)
            .values('stock__id', 'stock__name')
            .annotate(
                total_quantity=Sum('quantity_sold'),
                total_revenue=Sum(revenue_expression),
                last_sold=Max('date'),
                current_stock=Max('stock__quantity'),
            )
            .order_by('-total_revenue')
    )

    return render(request, 'store/sales_by_stock_report.html', {
        'report': report,
    })

def generate_receipt(request,pk):
    sale = get_object_or_404(Sale, pk=pk)
    
    return render(request, 'store/receipt.html', {'sale': sale})    
    return render(request, 'store/receipt.html', {'sale': sale})

@require_POST
def sale_delete(request, pk):
    """Delete a sale record and restore stock quantity"""
    sale = get_object_or_404(Sale, pk=pk)
    
    if sale.stock:
        # Restore stock quantity
        sale.stock.quantity += sale.quantity_sold
        sale.stock.save()
    
    sale.delete()
    messages.success(request, "Sale has been deleted and stock restored.")
    return redirect('sales_list')
