from django import forms
from .models import SchoolBudget, BudgetLineItem, BudgetPeriod, BudgetTransfer, BudgetDocument

class SchoolBudgetForm(forms.ModelForm):
    class Meta:
        model = SchoolBudget
        fields = [
            'school', 'budget_period', 'budget_title', 'description', 'total_budget_amount', 'allocated_amount', 'requesting_amount', 'status'
        ]
        widgets = {
            'school': forms.Select(attrs={'class': 'form-select'}),
            'budget_period': forms.Select(attrs={'class': 'form-select'}),
            'budget_title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'total_budget_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'id': 'id_total_budget_amount'}),
            'allocated_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'id': 'id_allocated_amount'}),
            'requesting_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'id': 'id_requesting_amount', 'readonly': 'readonly'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make requesting_amount read-only and add calculation attributes
        if 'requesting_amount' in self.fields:
            self.fields['requesting_amount'].help_text = "Automatically calculated (Total - Allocated)"
        
        # Update allocated_amount field label and help text
        if 'allocated_amount' in self.fields:
            self.fields['allocated_amount'].label = "Existing (Allocated Amount) (RWF)"
            self.fields['allocated_amount'].help_text = "Current allocated budget amount"

class BudgetLineItemForm(forms.ModelForm):
    class Meta:
        model = BudgetLineItem
        fields = [
            'budget_category', 'item_description', 'item_details', 'quantity', 'unit_cost', 'planned_date'
        ]

class BudgetPeriodForm(forms.ModelForm):
    class Meta:
        model = BudgetPeriod
        exclude = ['created_by', 'allocated_budget', 'spent_budget', 'is_closed', 'created_at', 'updated_at']
        widgets = {
            'period_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2025 Fiscal Year'}),
            'period_type': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'total_budget_limit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class BudgetTransferForm(forms.ModelForm):
    class Meta:
        model = BudgetTransfer
        fields = [
            'transfer_type',
            'source_line_item',
            'destination_line_item',
            'transfer_amount',
            'transfer_date',
            'reason',
        ]
        widgets = {
            'transfer_type': forms.Select(attrs={'class': 'form-select'}),
            'source_line_item': forms.Select(attrs={'class': 'form-select'}),
            'destination_line_item': forms.Select(attrs={'class': 'form-select'}),
            'transfer_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'transfer_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class BudgetDocumentForm(forms.ModelForm):
    document = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = BudgetDocument
        fields = ['criteria', 'document']
        widgets = {
            'criteria': forms.Select(attrs={'class': 'form-select'}),
        }

BudgetDocumentFormSet = forms.modelformset_factory(
    BudgetDocument,
    form=BudgetDocumentForm,
    extra=5,
    min_num=0,
    max_num=5,
    validate_min=False,
    validate_max=True,
    can_delete=False,
)