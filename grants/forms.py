from django import forms
from .models import GrantProposal, GrantCategory
from core.models import School
from reporting.models import ProposalCriterion
from .models import TotalGrantAllocation

class GrantProposalForm(forms.ModelForm):
    school = forms.ModelChoiceField(
        queryset=School.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, include_status=False, school_instance=None, force_school_field=False, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Make requested_amount read-only and add calculation attributes
        if 'requested_amount' in self.fields:
            self.fields['requested_amount'].widget.attrs.update({
                'readonly': 'readonly',
                'class': 'form-control',
                'id': 'id_requested_amount'
            })
            self.fields['requested_amount'].help_text = "Automatically calculated (Total - Current)"
        
        # Only show the school field if forced (for school admins without assignment)
        if not force_school_field:
            self.fields.pop('school')
            # If a school_instance is provided (for school admins), show as read-only
            if school_instance:
                self.fields['school_display'] = forms.CharField(
                    label='School',
                    initial=str(school_instance),
                    required=False,
                    widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'disabled': 'disabled'})
                )
        # Optionally include status field
        if not include_status and 'status' in self.fields:
            self.fields.pop('status')

    class Meta:
        model = GrantProposal
        fields = [
            'proposal_title', 'grant_category', 'description', 'objectives',
            'expected_outcomes', 'target_beneficiaries', 'total_amount', 'current_amount', 'requested_amount',
            'start_date', 'end_date', 'priority_level', 'status'
        ]
        widgets = {
            'total_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'id': 'id_total_amount'}),
            'current_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'id': 'id_current_amount'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class GrantCategoryForm(forms.ModelForm):
    class Meta:
        model = GrantCategory
        fields = ['category_name', 'category_type', 'description', 'min_amount', 'max_amount', 'priority_weight', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'category_name': forms.TextInput(attrs={'class': 'form-control'}),
            'category_type': forms.Select(attrs={'class': 'form-select'}),
            'min_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'priority_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class GrantProposalWithCriteriaForm(GrantProposalForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically add fields for all active proposal criteria
        for criterion in ProposalCriterion.objects.filter(active=True).order_by('ordering', 'name'):
            field_name = f'criterion_{criterion.id}'
            if criterion.type == 'file':
                self.fields[field_name] = forms.FileField(
                    label=criterion.name,
                    required=criterion.required,
                    help_text=criterion.description,
                )
            elif criterion.type == 'text':
                self.fields[field_name] = forms.CharField(
                    label=criterion.name,
                    required=criterion.required,
                    help_text=criterion.description,
                    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
                )
            elif criterion.type == 'boolean':
                self.fields[field_name] = forms.BooleanField(
                    label=criterion.name,
                    required=criterion.required,
                    help_text=criterion.description,
                )
            self.fields[field_name].criterion_obj = criterion


class TotalGrantAllocationForm(forms.ModelForm):
    """
    Form for system administrators to create and edit total grant allocations by year.
    """
    
    class Meta:
        model = TotalGrantAllocation
        fields = [
            'fiscal_year', 'total_budget', 'start_date', 'end_date', 
            'status', 'is_active', 'description', 'allocation_notes'
        ]
        widgets = {
            'fiscal_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '2020',
                'max': '2030',
                'placeholder': 'e.g., 2024'
            }),
            'total_budget': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': 'Enter total budget amount'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description of this allocation'
            }),
            'allocation_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Internal notes for administrators'
            }),
        }
    
    def clean_fiscal_year(self):
        """Validate that fiscal year is unique and reasonable."""
        fiscal_year = self.cleaned_data.get('fiscal_year')
        instance = getattr(self, 'instance', None)
        
        # Check if fiscal year already exists (excluding current instance)
        if TotalGrantAllocation.objects.filter(fiscal_year=fiscal_year).exclude(pk=instance.pk if instance else None).exists():
            raise forms.ValidationError(f"Fiscal year {fiscal_year} already exists.")
        
        # Validate reasonable range
        if fiscal_year < 2020 or fiscal_year > 2030:
            raise forms.ValidationError("Fiscal year must be between 2020 and 2030.")
        
        return fiscal_year
    
    def clean(self):
        """Validate that end_date is after start_date."""
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and end_date <= start_date:
            raise forms.ValidationError("End date must be after start date.")
        
        return cleaned_data 