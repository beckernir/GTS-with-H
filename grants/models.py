from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from core.models import User, School
import uuid


class GrantCategory(models.Model):
    """
    Model defining different categories of grants available for schools.
    """
    
    # Grant category types
    CATEGORY_TYPE_CHOICES = [
        ('infrastructure', 'Infrastructure Development'),
        ('academic', 'Academic Programs'),
        ('technology', 'Technology and ICT'),
        ('sports', 'Sports and Recreation'),
        ('library', 'Library and Resources'),
        ('laboratory', 'Laboratory Equipment'),
        ('maintenance', 'Maintenance and Repairs'),
        ('training', 'Teacher Training'),
        ('special_needs', 'Special Needs Support'),
        ('emergency', 'Emergency Response'),
        ('other', 'Other'),
    ]
    
    # Core fields
    category_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    category_name = models.CharField(max_length=100, unique=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPE_CHOICES, default='other')
    description = models.TextField()
    
    # Grant limits and rules
    min_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    priority_weight = models.DecimalField(max_digits=3, decimal_places=2, default=1.00, help_text="Weight for AI allocation (0.00-1.00)")
    
    # Category status
    is_active = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_grant_categories')
    
    class Meta:
        db_table = 'grants_grant_category'
        verbose_name = 'Grant Category'
        verbose_name_plural = 'Grant Categories'
        ordering = ['category_name']
    
    def __str__(self):
        return f"{self.category_name} ({self.get_category_type_display()})"


class GrantProposal(models.Model):
    """
    Model for grant proposals submitted by schools to REB.
    """
    
    # Proposal status choices
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted for Review'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('funded', 'Funded'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Priority levels
    PRIORITY_CHOICES = [
        ('low', 'Low Priority'),
        ('medium', 'Medium Priority'),
        ('high', 'High Priority'),
        ('urgent', 'Urgent'),
    ]
    
    # Core proposal fields
    proposal_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    proposal_title = models.CharField(max_length=200)
    proposal_code = models.CharField(max_length=20, unique=True, help_text="Auto-generated proposal code")
    
    # School and category information
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='grant_proposals')
    grant_category = models.ForeignKey(GrantCategory, on_delete=models.CASCADE, related_name='proposals')
    
    # Proposal details
    description = models.TextField()
    objectives = models.TextField()
    expected_outcomes = models.TextField()
    target_beneficiaries = models.TextField()
    
    # Financial information
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text="Total project cost")
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text="Current allocated budget amount")
    requested_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    allocated_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    disbursed_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Timeline and priority
    start_date = models.DateField()
    end_date = models.DateField()
    priority_level = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Status and workflow
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    submission_date = models.DateTimeField(blank=True, null=True)
    approval_date = models.DateTimeField(blank=True, null=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    
    # Review and approval
    review_notes = models.TextField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)
    
    # AI allocation scores
    ai_priority_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    ai_need_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    ai_impact_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_proposals')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_proposals')
    
    class Meta:
        db_table = 'grants_grant_proposal'
        verbose_name = 'Grant Proposal'
        verbose_name_plural = 'Grant Proposals'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.proposal_title} - {self.school.school_name}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate total_amount if it's 0 and requested_amount exists
        if self.total_amount == 0 and self.requested_amount and self.requested_amount > 0:
            self.total_amount = self.requested_amount
        
        if not self.pk:
            super().save(*args, **kwargs)  # Save first to get an ID
            self.proposal_code = f"GP{timezone.now().strftime('%Y%m')}{self.id:04d}"
            super().save(update_fields=['proposal_code'])  # Save again to update the code
        else:
            super().save(*args, **kwargs)
    
    def get_duration_days(self):
        """Calculate proposal duration in days."""
        return (self.end_date - self.start_date).days
    
    def get_completion_percentage(self):
        """Calculate completion percentage based on disbursed vs allocated amount."""
        if self.allocated_amount > 0:
            return (self.disbursed_amount / self.allocated_amount) * 100
        return 0
    
    def get_ai_total_score(self):
        """Calculate total AI score for allocation."""
        return (self.ai_priority_score + self.ai_need_score + self.ai_impact_score) / 3

    def get_status_color(self):
        """Return Bootstrap color class based on proposal status."""
        status_colors = {
            'draft': 'secondary',
            'submitted': 'info',
            'under_review': 'warning',
            'approved': 'success',
            'rejected': 'danger',
            'funded': 'primary',
            'completed': 'success',
            'cancelled': 'dark',
        }
        return status_colors.get(self.status, 'secondary')

    def get_status_description(self):
        """Return description of the current proposal status."""
        status_descriptions = {
            'draft': 'Proposal is in draft stage and can be edited',
            'submitted': 'Proposal has been submitted for review',
            'under_review': 'Proposal is currently under review',
            'approved': 'Proposal has been approved and is ready for funding',
            'rejected': 'Proposal has been rejected',
            'funded': 'Proposal has been funded and implementation can begin',
            'completed': 'Proposal implementation has been completed',
            'cancelled': 'Proposal has been cancelled',
        }
        return status_descriptions.get(self.status, 'Unknown status')

    @property
    def progress_percentage(self):
        """Calculate implementation progress percentage."""
        if self.status == 'completed':
            return 100
        elif self.status == 'funded':
            return 75
        elif self.status == 'approved':
            return 50
        elif self.status == 'under_review':
            return 25
        elif self.status == 'submitted':
            return 10
        else:
            return 0

    @property
    def effective_total_amount(self):
        """Return total_amount, or requested_amount if total_amount is 0."""
        if self.total_amount == 0 and self.requested_amount and self.requested_amount > 0:
            return self.requested_amount
        return self.total_amount


class ProposalDocument(models.Model):
    """
    Model for documents attached to grant proposals.
    """
    
    # Document types
    DOCUMENT_TYPE_CHOICES = [
        ('proposal', 'Proposal Document'),
        ('budget', 'Budget Breakdown'),
        ('supporting', 'Supporting Documents'),
        ('approval', 'Approval Documents'),
        ('completion', 'Completion Report'),
        ('other', 'Other'),
    ]
    
    # Core fields
    document_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    proposal = models.ForeignKey(GrantProposal, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, default='other')
    document_title = models.CharField(max_length=200)
    document_file = models.FileField(upload_to='proposal_documents/')
    file_size = models.PositiveIntegerField(help_text="File size in bytes")
    
    # Document metadata
    description = models.TextField(blank=True, null=True)
    is_required = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    ocr_text = models.TextField(blank=True, null=True, help_text="Extracted text from OCR analysis.")
    
    # Audit fields
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_documents')
    
    class Meta:
        db_table = 'grants_proposal_document'
        verbose_name = 'Proposal Document'
        verbose_name_plural = 'Proposal Documents'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.document_title} - {self.proposal.proposal_title}"


class ProposalBudget(models.Model):
    """
    Detailed budget breakdown for grant proposals.
    """
    
    # Budget item categories
    ITEM_CATEGORY_CHOICES = [
        ('personnel', 'Personnel Costs'),
        ('equipment', 'Equipment and Materials'),
        ('infrastructure', 'Infrastructure'),
        ('services', 'Services and Contracts'),
        ('travel', 'Travel and Transportation'),
        ('utilities', 'Utilities and Maintenance'),
        ('other', 'Other Costs'),
    ]
    
    # Core fields
    budget_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    proposal = models.ForeignKey(GrantProposal, on_delete=models.CASCADE, related_name='budget_items')
    item_category = models.CharField(max_length=20, choices=ITEM_CATEGORY_CHOICES, default='other')
    item_description = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Budget tracking
    allocated_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    spent_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_budget_items')
    
    class Meta:
        db_table = 'grants_proposal_budget'
        verbose_name = 'Proposal Budget Item'
        verbose_name_plural = 'Proposal Budget Items'
        ordering = ['item_category', 'item_description']
    
    def __str__(self):
        return f"{self.item_description} - {self.proposal.proposal_title}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate total cost
        self.total_cost = self.quantity * self.unit_cost
        super().save(*args, **kwargs)
    
    def get_spending_percentage(self):
        """Calculate spending percentage for this budget item."""
        if self.allocated_amount > 0:
            return (self.spent_amount / self.allocated_amount) * 100
        return 0


class FundAllocation(models.Model):
    """
    Model for tracking fund allocations and disbursements.
    """
    
    # Allocation types
    ALLOCATION_TYPE_CHOICES = [
        ('initial', 'Initial Allocation'),
        ('supplementary', 'Supplementary Allocation'),
        ('adjustment', 'Budget Adjustment'),
        ('final', 'Final Disbursement'),
    ]
    
    # Core fields
    allocation_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    proposal = models.ForeignKey(GrantProposal, on_delete=models.CASCADE, related_name='fund_allocations')
    allocation_type = models.CharField(max_length=20, choices=ALLOCATION_TYPE_CHOICES, default='initial')
    
    # Financial details
    allocated_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    disbursed_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    allocation_date = models.DateField()
    disbursement_date = models.DateField(blank=True, null=True)
    
    # Allocation details
    allocation_notes = models.TextField(blank=True, null=True)
    disbursement_notes = models.TextField(blank=True, null=True)
    
    # AI allocation data
    ai_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    ai_factors = models.JSONField(default=dict, help_text="JSON object containing AI allocation factors")
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    allocated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='made_allocations')
    disbursed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='made_disbursements')
    
    class Meta:
        db_table = 'grants_fund_allocation'
        verbose_name = 'Fund Allocation'
        verbose_name_plural = 'Fund Allocations'
        ordering = ['-allocation_date']
    
    def __str__(self):
        return f"{self.proposal.proposal_title} - {self.allocated_amount} RWF"
    
    def get_disbursement_percentage(self):
        """Calculate disbursement percentage."""
        if self.allocated_amount > 0:
            return (self.disbursed_amount / self.allocated_amount) * 100
        return 0


class ProposalReview(models.Model):
    """
    Model for tracking proposal review process and decisions.
    """
    
    # Review status choices
    REVIEW_STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('in_progress', 'Review In Progress'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('requires_changes', 'Requires Changes'),
    ]
    
    # Core fields
    review_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    proposal = models.ForeignKey(GrantProposal, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposal_reviews')
    
    # Review details
    review_status = models.CharField(max_length=20, choices=REVIEW_STATUS_CHOICES, default='pending')
    review_notes = models.TextField()
    technical_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Technical merit score (0-100)")
    feasibility_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Feasibility score (0-100)")
    impact_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Impact potential score (0-100)")
    
    # Review timeline
    review_start_date = models.DateTimeField()
    review_completion_date = models.DateTimeField(blank=True, null=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'grants_proposal_review'
        verbose_name = 'Proposal Review'
        verbose_name_plural = 'Proposal Reviews'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review of {self.proposal.proposal_title} by {self.reviewer.get_full_name()}"
    
    def get_total_score(self):
        """Calculate total review score."""
        return (self.technical_score + self.feasibility_score + self.impact_score) / 3


class TotalGrantAllocation(models.Model):
    """
    Model for system administrators to set total grant allocations by year.
    This allows tracking of annual budget limits and allocations.
    """
    
    # Allocation status choices
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('archived', 'Archived'),
    ]
    
    # Core fields
    allocation_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    fiscal_year = models.PositiveIntegerField(unique=True, help_text="Fiscal year (e.g., 2024)")
    total_budget = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0.01)], help_text="Total grant budget for the year")
    
    # Allocation details
    allocated_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, help_text="Amount already allocated to proposals")
    disbursed_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, help_text="Amount already disbursed")
    
    # Status and management
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_active = models.BooleanField(default=True, help_text="Whether this allocation is currently active")
    
    # Notes and description
    description = models.TextField(blank=True, null=True, help_text="Additional notes about this allocation")
    allocation_notes = models.TextField(blank=True, null=True, help_text="Internal notes for administrators")
    
    # Timeline
    start_date = models.DateField(help_text="Start date of the fiscal year")
    end_date = models.DateField(help_text="End date of the fiscal year")
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_grant_allocations')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_grant_allocations')
    
    class Meta:
        db_table = 'grants_total_grant_allocation'
        verbose_name = 'Total Grant Allocation'
        verbose_name_plural = 'Total Grant Allocations'
        ordering = ['-fiscal_year']
    
    def __str__(self):
        return f"FY {self.fiscal_year} - {self.total_budget} RWF"
    
    def get_remaining_budget(self):
        """Calculate remaining budget for allocation."""
        return self.total_budget - self.allocated_amount
    
    def get_allocation_percentage(self):
        """Calculate percentage of budget allocated."""
        if self.total_budget > 0:
            return (self.allocated_amount / self.total_budget) * 100
        return 0
    
    def get_disbursement_percentage(self):
        """Calculate percentage of budget disbursed."""
        if self.total_budget > 0:
            return (self.disbursed_amount / self.total_budget) * 100
        return 0
    
    def get_utilization_percentage(self):
        """Calculate percentage of allocated budget utilized."""
        if self.allocated_amount > 0:
            return (self.disbursed_amount / self.allocated_amount) * 100
        return 0
    
    def can_allocate(self, amount):
        """Check if a given amount can be allocated within this budget."""
        return self.get_remaining_budget() >= amount
    
    def is_over_allocated(self):
        """Check if the allocation is over the budget limit."""
        return self.allocated_amount > self.total_budget
