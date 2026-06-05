from django import forms
# from django.contrib.auth.forms import UserCreationForm
from .models import Stock
from .models import Supplier

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        exclude = ['date', 'is_deleted']
        widgets = {
            'total_cost': forms.NumberInput(attrs={
                'readonly': 'readonly',
                'step': '0.01',
            }),
            'quantity': forms.NumberInput(attrs={
                'min': '1',
            }),
            'total_cost': forms.NumberInput(attrs={
                'readonly': 'readonly',
                'step': '0.01',
            }),
        }
        error_messages = {
            'quantity': {
                'min_value': 'Quantity must be at least 1.',
            },
            'total_cost': {
                'min_value': 'Total cost cannot be negative.',
            },
        }

class StockRestockForm(forms.Form):
    quantity_added = forms.IntegerField(min_value=1, label='Quantity to add', initial=1)
    unit_cost = forms.DecimalField(max_digits=20, decimal_places=2, required=False)
    unit_price = forms.DecimalField(max_digits=20, decimal_places=2, required=False)

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"