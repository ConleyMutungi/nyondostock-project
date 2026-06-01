from django import forms
from .models import Sale, Expense

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer_name', 'stock', 'quantity_sold', 'delivery_distance']
        widgets = {
            'delivery_distance': forms.NumberInput(attrs={'step': '0.01', 'min': '0.00'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delivery_distance'].label = 'Delivery distance (km)'
        self.fields['delivery_distance'].widget.attrs.update({'placeholder': 'e.g., 3.5'})

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = "__all__"
        widgets = {
            'total_amount': forms.NumberInput(attrs={
                'readonly': 'readonly',
                'step': '0.01',
            }),
        }
