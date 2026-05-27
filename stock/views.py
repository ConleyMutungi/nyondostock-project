from django.shortcuts import render, redirect, get_object_or_404
from .forms import SupplierForm
from .models import Supplier
from .models import Stock
from .forms import StockForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def supplier_reg_form(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_registration_form')
        
    else:
        form = SupplierForm()
    context = {
        'form' : form
    }    
    return render(request,'store/supplier_reg_form.html', {'form':form})    

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
    context = {
        'form' : form
    }    
    return render(request,'store/stock_reg_form.html', {'form':form}) 

def stock_list(request):
    stocks = Stock.objects.all()
    return render(request, 'store/stock_list.html', {'stocks': stocks})

def delete_supplier(request,pk):
    supplier = get_object_or_404(Supplier,pk=pk)
    supplier.delete()
    return redirect('supplier_list')       