from django import forms
from .models import Tender, TenderDocument, Bid
from reporting.models import SupplierCriterion

class TenderForm(forms.ModelForm):
    class Meta:
        model = Tender
        fields = ['title', 'description', 'status', 'school', 'submission_deadline', 'awarded_to']
        widgets = {
            'submission_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class TenderDocumentForm(forms.ModelForm):
    class Meta:
        model = TenderDocument
        fields = ['document_type', 'document_title', 'document_file', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['proposal_text', 'document']
        widgets = {
            'proposal_text': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class BidWithCriteriaForm(BidForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically add fields for all active supplier criteria
        for criterion in SupplierCriterion.objects.filter(active=True).order_by('ordering', 'name'):
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