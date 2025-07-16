from django import forms
from .models import Tender, TenderDocument, Bid

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