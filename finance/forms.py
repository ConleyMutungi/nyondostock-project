from django import forms
from .models import Sale, Expense

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = "__all__"

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
