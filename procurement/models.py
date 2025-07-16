from django.db import models
from core.models import User, School
import uuid

class Tender(models.Model):
    """Model for procurement tenders."""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('open', 'Open for Submission'),
        ('closed', 'Closed'),
        ('awarded', 'Awarded'),
        ('cancelled', 'Cancelled'),
    ]
    tender_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True, related_name='tenders')
    published_at = models.DateTimeField(blank=True, null=True)
    submission_deadline = models.DateTimeField()
    awarded_to = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tenders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TenderDocument(models.Model):
    """Supporting documents for tenders."""
    DOCUMENT_TYPE_CHOICES = [
        ('specification', 'Specification'),
        ('bid', 'Bid Submission'),
        ('award', 'Award Letter'),
        ('other', 'Other'),
    ]
    document_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, default='other')
    document_title = models.CharField(max_length=200)
    document_file = models.FileField(upload_to='tender_documents/')
    file_size = models.PositiveIntegerField(help_text="File size in bytes")
    description = models.TextField(blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_tender_documents')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    ocr_text = models.TextField(blank=True, null=True, help_text="Extracted text from OCR analysis.")

    def __str__(self):
        return f"{self.document_title} - {self.tender.title}"

class TenderStatusHistory(models.Model):
    """Track status changes for tenders."""
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE, related_name='status_history')
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tender_status_changes')
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tender.title}: {self.old_status} → {self.new_status} at {self.changed_at}"

class Bid(models.Model):
    """Model for supplier bids on tenders."""
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('reviewed', 'Reviewed'),
        ('awarded', 'Awarded'),
        ('rejected', 'Rejected'),
    ]
    bid_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE, related_name='bids')
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    proposal_text = models.TextField()
    document = models.FileField(upload_to='bid_documents/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    awarded_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Bid by {str(self.supplier)} for {str(self.tender)}"
