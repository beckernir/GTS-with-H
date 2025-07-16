from django import forms
from .models import REBGrantBudget

class REBGrantBudgetForm(forms.ModelForm):
    class Meta:
        model = REBGrantBudget
        fields = ['year', 'total_amount', 'notes']
        widgets = {
            'year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2025'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Total Grant Amount'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional notes'}),
        } 