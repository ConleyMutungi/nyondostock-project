from django.shortcuts import render, redirect, get_object_or_404
from .forms import SupplierForm
from .models import Supplier
from .models import Stock
from .forms import StockForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def supplier_reg_form(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_reg_form')
        
    else:
        form = SupplierForm()
    context = {
        'form' : form
    }    
    return render(request,'store/supplier_reg_form.html', {'form':form})    

def supplier_list(request):
    supplier = Supplier.objects.all()
    return render (request, 'store/supplier_list.html', {'supplier':supplier})

def stock_reg_form(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock_reg_form')
        
    else:
        form = StockForm()
    context = {
        'form' : form
    }    
    return render(request,'store/stock_reg_form.html', {'form':form}) 

def stock_list(request):
    stock = Stock.objects.all()
    return render (request, 'store/stock_list.html', {'stock':stock})

def delete_supplier(request,pk):
    supplier = get_object_or_404(Supplier,pk=pk)
    supplier.delete()
    return redirect('supplier_list')       