from django import forms
# from django.contrib.auth.forms import UserCreationForm
from .models import Stock
from .models import Supplier

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = "__all__"

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"