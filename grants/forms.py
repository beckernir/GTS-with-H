from django import forms
from .models import GrantProposal, GrantCategory
from core.models import School

class GrantProposalForm(forms.ModelForm):
    school = forms.ModelChoiceField(
        queryset=School.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = GrantProposal
        fields = [
            'proposal_title', 'grant_category', 'description', 'objectives',
            'expected_outcomes', 'target_beneficiaries', 'requested_amount',
            'start_date', 'end_date', 'priority_level', 'status'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Only show the school field for system admins or REB officers
        if not (user and (getattr(user, 'is_system_admin', lambda: False)() or getattr(user, 'is_reb_officer', lambda: False)())):
            self.fields.pop('school')

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