from django import forms
# from django.contrib.auth.forms import UserCreationForm
from .models import Stock
from .models import Supplier

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = "__all__"
        widgets = {
            'total_cost': forms.NumberInput(attrs={
                'readonly': 'readonly',
                'step': '0.01',
            }),
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"