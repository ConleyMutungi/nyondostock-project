from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .forms import StockForm, SupplierForm
from .models import Stock, Supplier

@login_required
def supplier_reg_form(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_registration_form')
    else:
        form = SupplierForm()

    return render(request, 'store/supplier_reg_form.html', {'form': form})


def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'store/supplier_list.html', {'suppliers': suppliers})


def stock_reg_form(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock_registration_form')
    else:
        form = StockForm()

    return render(request, 'store/stock_reg_form.html', {'form': form})


def stock_list(request):
    stocks = Stock.objects.all()
    return render(request, 'store/stock_list.html', {'stocks': stocks})

def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.delete()
    return redirect('supplier_list')


def stock_detail(request, pk):
    stock = get_object_or_404(Stock.all_objects, pk=pk)
    return render(request, 'store/stock_detail.html', {'stock': stock})


def stock_edit(request, pk):
    stock = get_object_or_404(Stock.all_objects, pk=pk)
    return render(request, 'store/stock_form.html', {'stock': stock})


@require_POST
def stock_delete(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    stock.quantity = 0
    stock.save()
    messages.warning(request, f"'{stock.name}' has been successfully archived to Out of Stock.")
    return redirect('stock_list')

def stock_delete(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    stock.delete()
    return redirect('stock_list')

# @require_POST
# def stock_restore(request, pk):
#     stock = get_object_or_404(Stock.all_objects, pk=pk)
#     quantity_to_add = int(request.POST.get('quantity', 1))

#     if quantity_to_add > 0:
#         stock.quantity = quantity_to_add
#         stock.is_deleted = False
#         stock.deleted_at = None
#         stock.save()
#         messages.success(request, f"Restored '{stock.name}' with {quantity_to_add} new units.")
#     else:
#         messages.error(request, "Restock count must exceed 0.")

#     return redirect('stock_list')
