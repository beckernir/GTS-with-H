from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from core.models import User, School
from grants.models import GrantProposal
import uuid


class BudgetPeriod(models.Model):
    """
    Model for defining budget periods (fiscal years, quarters, etc.).
    """
    
    # Period types
    PERIOD_TYPE_CHOICES = [
        ('fiscal_year', 'Fiscal Year'),
        ('quarter', 'Quarter'),
        ('semester', 'Semester'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom Period'),
    ]
    
    # Core fields
    period_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    period_name = models.CharField(max_length=100, unique=True)
    period_type = models.CharField(max_length=20, choices=PERIOD_TYPE_CHOICES, default='fiscal_year')
    
    # Period dates
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Budget limits
    total_budget_limit = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    allocated_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    spent_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    # Period status
    is_active = models.BooleanField(default=True)
    is_closed = models.BooleanField(default=False)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_budget_periods')
    
    class Meta:
        db_table = 'budget_budget_period'
        verbose_name = 'Budget Period'
        verbose_name_plural = 'Budget Periods'
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.period_name} ({self.start_date} - {self.end_date})"
    
    def get_remaining_budget(self):
        """Calculate remaining budget for the period."""
        return self.total_budget_limit - self.spent_budget
    
    def get_utilization_percentage(self):
        """Calculate budget utilization percentage."""
        if self.total_budget_limit > 0:
            return (self.spent_budget / self.total_budget_limit) * 100
        return 0
    
    def is_current_period(self):
        """Check if this is the current active period."""
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date and self.is_active


class SchoolBudget(models.Model):
    """
    Model for school-specific budget allocations and tracking.
    """
    
    # Budget status choices
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Core fields
    budget_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='budgets')
    budget_period = models.ForeignKey(BudgetPeriod, on_delete=models.CASCADE, related_name='school_budgets')
    
    # Budget details
    budget_title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Financial information
    total_budget_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0.01)])
    allocated_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    spent_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    committed_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    # Budget timeline
    submission_date = models.DateTimeField(blank=True, null=True)
    approval_date = models.DateTimeField(blank=True, null=True)
    activation_date = models.DateTimeField(blank=True, null=True)
    closure_date = models.DateTimeField(blank=True, null=True)
    
    # Budget notes
    approval_notes = models.TextField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_school_budgets')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_school_budgets')
    
    class Meta:
        db_table = 'budget_school_budget'
        verbose_name = 'School Budget'
        verbose_name_plural = 'School Budgets'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.budget_title} - {self.school.school_name}"
    
    def get_available_budget(self):
        """Calculate available budget (allocated - spent - committed)."""
        return self.allocated_amount - self.spent_amount - self.committed_amount
    
    def get_spending_percentage(self):
        """Calculate spending percentage."""
        if self.allocated_amount > 0:
            return (self.spent_amount / self.allocated_amount) * 100
        return 0
    
    def get_commitment_percentage(self):
        """Calculate commitment percentage."""
        if self.allocated_amount > 0:
            return (self.committed_amount / self.allocated_amount) * 100
        return 0


class BudgetCategory(models.Model):
    """
    Model for budget categories and line items.
    """
    
    # Category types
    CATEGORY_TYPE_CHOICES = [
        ('personnel', 'Personnel Costs'),
        ('equipment', 'Equipment and Materials'),
        ('infrastructure', 'Infrastructure'),
        ('services', 'Services and Contracts'),
        ('travel', 'Travel and Transportation'),
        ('utilities', 'Utilities and Maintenance'),
        ('training', 'Training and Development'),
        ('supplies', 'Supplies and Consumables'),
        ('technology', 'Technology and ICT'),
        ('other', 'Other Costs'),
    ]
    
    # Core fields
    category_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    category_name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPE_CHOICES, default='other')
    description = models.TextField(blank=True, null=True)
    
    # Budget limits
    budget_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    allocated_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    spent_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Category settings
    is_active = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=False)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'budget_budget_category'
        verbose_name = 'Budget Category'
        verbose_name_plural = 'Budget Categories'
        ordering = ['category_type', 'category_name']
    
    def __str__(self):
        return f"{self.category_name} ({self.get_category_type_display()})"
    
    def get_remaining_budget(self):
        """Calculate remaining budget for this category."""
        return self.budget_limit - self.spent_amount
    
    def get_utilization_percentage(self):
        """Calculate budget utilization percentage."""
        if self.budget_limit > 0:
            return (self.spent_amount / self.budget_limit) * 100
        return 0


class BudgetLineItem(models.Model):
    """
    Model for individual budget line items within a school budget.
    """
    
    # Line item status choices
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Core fields
    line_item_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    school_budget = models.ForeignKey(SchoolBudget, on_delete=models.CASCADE, related_name='line_items')
    budget_category = models.ForeignKey(BudgetCategory, on_delete=models.CASCADE, related_name='line_items')
    
    # Line item details
    item_description = models.CharField(max_length=200)
    item_details = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Financial tracking
    allocated_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    spent_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    committed_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Status and timeline
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    planned_date = models.DateField()
    completion_date = models.DateField(blank=True, null=True)
    
    # Related grant proposal (if applicable)
    related_proposal = models.ForeignKey(GrantProposal, on_delete=models.SET_NULL, null=True, blank=True, related_name='budget_line_items')
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_budget_line_items')
    
    class Meta:
        db_table = 'budget_budget_line_item'
        verbose_name = 'Budget Line Item'
        verbose_name_plural = 'Budget Line Items'
        ordering = ['budget_category', 'item_description']
    
    def __str__(self):
        return f"{self.item_description} - {self.school_budget.budget_title}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate total cost
        self.total_cost = self.quantity * self.unit_cost
        super().save(*args, **kwargs)
    
    def get_spending_percentage(self):
        """Calculate spending percentage for this line item."""
        if self.allocated_amount > 0:
            return (self.spent_amount / self.allocated_amount) * 100
        return 0
    
    def get_remaining_budget(self):
        """Calculate remaining budget for this line item."""
        return self.allocated_amount - self.spent_amount - self.committed_amount


class Expenditure(models.Model):
    """
    Model for tracking actual expenditures against budget line items.
    """
    
    # Expenditure types
    EXPENDITURE_TYPE_CHOICES = [
        ('actual', 'Actual Expenditure'),
        ('commitment', 'Commitment'),
        ('adjustment', 'Budget Adjustment'),
        ('transfer', 'Budget Transfer'),
    ]
    
    # Payment methods
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('check', 'Check'),
        ('mobile_money', 'Mobile Money'),
        ('other', 'Other'),
    ]
    
    # Core fields
    expenditure_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    budget_line_item = models.ForeignKey(BudgetLineItem, on_delete=models.CASCADE, related_name='expenditures')
    
    # Expenditure details
    expenditure_type = models.CharField(max_length=20, choices=EXPENDITURE_TYPE_CHOICES, default='actual')
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    description = models.CharField(max_length=200)
    details = models.TextField(blank=True, null=True)
    
    # Payment information
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='bank_transfer')
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateField()
    
    # Supplier/vendor information
    supplier_name = models.CharField(max_length=200, blank=True, null=True)
    supplier_contact = models.CharField(max_length=100, blank=True, null=True)
    
    # Supporting documents
    receipt_number = models.CharField(max_length=50, blank=True, null=True)
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_expenditures')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_expenditures')
    
    class Meta:
        db_table = 'budget_expenditure'
        verbose_name = 'Expenditure'
        verbose_name_plural = 'Expenditures'
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"{self.description} - {self.amount} RWF"


class BudgetTransfer(models.Model):
    """
    Model for tracking budget transfers between line items or categories.
    """
    
    # Transfer types
    TRANSFER_TYPE_CHOICES = [
        ('within_category', 'Within Category'),
        ('between_categories', 'Between Categories'),
        ('between_budgets', 'Between Budgets'),
        ('adjustment', 'Budget Adjustment'),
    ]
    
    # Core fields
    transfer_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    transfer_type = models.CharField(max_length=20, choices=TRANSFER_TYPE_CHOICES, default='within_category')
    
    # Source and destination
    source_line_item = models.ForeignKey(BudgetLineItem, on_delete=models.CASCADE, related_name='outgoing_transfers')
    destination_line_item = models.ForeignKey(BudgetLineItem, on_delete=models.CASCADE, related_name='incoming_transfers')
    
    # Transfer details
    transfer_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    transfer_date = models.DateField()
    reason = models.TextField()
    
    # Approval and status
    is_approved = models.BooleanField(default=False)
    approval_date = models.DateTimeField(blank=True, null=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_transfers')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_transfers')
    
    class Meta:
        db_table = 'budget_budget_transfer'
        verbose_name = 'Budget Transfer'
        verbose_name_plural = 'Budget Transfers'
        ordering = ['-transfer_date']
    
    def __str__(self):
        return f"Transfer of {self.transfer_amount} RWF from {self.source_line_item} to {self.destination_line_item}"


class BudgetReport(models.Model):
    """
    Model for storing budget reports and analytics.
    """
    
    # Report types
    REPORT_TYPE_CHOICES = [
        ('monthly', 'Monthly Report'),
        ('quarterly', 'Quarterly Report'),
        ('annual', 'Annual Report'),
        ('variance', 'Variance Analysis'),
        ('forecast', 'Budget Forecast'),
        ('custom', 'Custom Report'),
    ]
    
    # Core fields
    report_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES, default='monthly')
    report_title = models.CharField(max_length=200)
    
    # Report scope
    school_budget = models.ForeignKey(SchoolBudget, on_delete=models.CASCADE, related_name='reports')
    report_period_start = models.DateField()
    report_period_end = models.DateField()
    
    # Report content
    report_data = models.JSONField(default=dict, help_text="JSON object containing report data")
    summary = models.TextField(blank=True, null=True)
    
    # Report file
    report_file = models.FileField(upload_to='budget_reports/', blank=True, null=True)
    
    # Audit fields
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_budget_reports')
    
    class Meta:
        db_table = 'budget_budget_report'
        verbose_name = 'Budget Report'
        verbose_name_plural = 'Budget Reports'
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.report_title} - {self.school_budget.budget_title}"
