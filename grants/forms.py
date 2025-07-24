from django import forms
from .models import GrantProposal, GrantCategory
from core.models import School
from reporting.models import ProposalCriterion

class GrantProposalForm(forms.ModelForm):
    school = forms.ModelChoiceField(
        queryset=School.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, include_status=False, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Only show the school field for system admins or REB officers
        if not (user and (getattr(user, 'is_system_admin', lambda: False)() or getattr(user, 'is_reb_officer', lambda: False)())):
            self.fields.pop('school')
        # Optionally include status field
        if not include_status and 'status' in self.fields:
            self.fields.pop('status')

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