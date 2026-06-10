from django import forms
from .models import Sale, Expense
from stock.models import Stock

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer_name', 'stock', 'quantity_sold', 'delivery_distance']
        widgets = {
            'delivery_distance': forms.NumberInput(attrs={'step': '0.01', 'min': '0.00'}),
        }
        error_messages = {
            'quantity_sold': {
                'min_value': 'Quantity sold must be at least 1.',
            },
            'delivery_distance': {
                'min_value': 'Delivery distance cannot be negative.',
            },
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delivery_distance'].label = 'Delivery distance (km)'
        self.fields['delivery_distance'].widget.attrs.update({'placeholder': 'e.g., 3.5'})

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['stock', 'price', 'transport_cost', 'tax_amount', 'total_amount', 'Comments']
        widgets = {
            'price': forms.NumberInput(attrs={
                'readonly': 'readonly',
                'step': '0.01',
            }),
            'total_amount': forms.NumberInput(attrs={
                'readonly': 'readonly',
                'step': '0.01',
            }),
        }
        error_messages = {
            'total_amount': {
                'min_value': 'Total amount cannot be negative.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.order_by('name')
        self.fields['stock'].required = True
        self.fields['stock'].label = 'Stock item'
        self.fields['price'].label = 'Purchase price'
        self.fields['price'].help_text = 'Automatically uses the selected stock item purchase price.'
