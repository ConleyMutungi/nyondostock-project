from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .forms import StockForm, StockRestockForm, SupplierForm
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


def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    # If Supplier.stock_supplied references a Stock, include it; allow reverse lookup if model changes later
    stock_item = supplier.stock_supplied
    return render(request, 'store/supplier_detail.html', {'supplier': supplier, 'stock_item': stock_item})


def stock_reg_form(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            quantity_added = form.cleaned_data.get('quantity', 0)
            
            # Check if stock with this name already exists
            existing_stock = Stock.objects.filter(name=name, is_deleted=False).first()
            
            if existing_stock:
                # Add to existing stock quantity
                existing_stock.quantity += quantity_added
                existing_stock.unit_cost = form.cleaned_data.get('unit_cost', existing_stock.unit_cost)
                existing_stock.unit_price = form.cleaned_data.get('unit_price', existing_stock.unit_price)
                existing_stock.is_on_credit = form.cleaned_data.get('is_on_credit', existing_stock.is_on_credit)
                existing_stock.is_paid = form.cleaned_data.get('is_paid', existing_stock.is_paid)
                existing_stock.save()
                messages.success(request, f"Added {quantity_added} units to '{name}'. New total: {existing_stock.quantity} units")
            else:
                # Create new stock entry
                form.save()
                messages.success(request, f"New stock '{name}' registered successfully with {quantity_added} units")
            
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
    suppliers = Supplier.objects.filter(stock_supplied=stock)
    return render(request, 'store/stock_detail.html', {'stock': stock, 'suppliers': suppliers})


def stock_restock(request, pk):
    stock = get_object_or_404(Stock.all_objects, pk=pk)
    if request.method == 'POST':
        form = StockRestockForm(request.POST)
        if form.is_valid():
            quantity_added = form.cleaned_data['quantity_added']
            stock.quantity = (stock.quantity or 0) + quantity_added
            stock.unit_cost = form.cleaned_data.get('unit_cost') or stock.unit_cost
            stock.unit_price = form.cleaned_data.get('unit_price') or stock.unit_price
            stock.save()
            messages.success(request, f"Restocked {quantity_added} units of '{stock.name}'. New total: {stock.quantity} units")
            return redirect('stock_detail', pk=stock.pk)
    else:
        form = StockRestockForm(initial={
            'unit_cost': stock.unit_cost,
            'unit_price': stock.unit_price,
        })

    return render(request, 'store/stock_restock_form.html', {
        'form': form,
        'stock': stock,
    })


def stock_edit(request, pk):
    stock = get_object_or_404(Stock.all_objects, pk=pk)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            messages.success(request, f"Stock '{stock.name}' was updated successfully.")
            return redirect('stock_detail', pk=stock.pk)
    else:
        form = StockForm(instance=stock)

    return render(request, 'store/stock_form.html', {'form': form, 'stock': stock})


@require_POST
def stock_delete(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    stock.is_deleted = True
    stock.save()
    messages.warning(request, f"'{stock.name}' has been successfully archived.")
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
