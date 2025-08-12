from django.contrib import admin
from .models import SchoolBudget
from .models import BudgetDocument

# Register your models here.

@admin.register(SchoolBudget)
class SchoolBudgetAdmin(admin.ModelAdmin):
    list_display = ['budget_title', 'school', 'budget_period', 'total_budget_amount', 'allocated_amount', 'requesting_amount', 'status', 'created_at']
    list_filter = ['status', 'budget_period', 'school']
    search_fields = ['budget_title', 'school__school_name']
    readonly_fields = ['budget_id', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Info', {'fields': ('budget_title', 'school', 'budget_period')}),
        ('Amounts', {'fields': ('total_budget_amount', 'allocated_amount', 'requesting_amount', 'spent_amount', 'committed_amount')}),
        ('Status', {'fields': ('status', 'submission_date', 'approval_date', 'activation_date', 'closure_date')}),
        ('Notes', {'fields': ('approval_notes', 'rejection_reason')}),
        ('Audit', {'fields': ('created_by', 'approved_by', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

@admin.register(BudgetDocument)
class BudgetDocumentAdmin(admin.ModelAdmin):
    list_display = ['school_budget', 'criteria', 'document', 'uploaded_at']
    list_filter = ['criteria', 'uploaded_at']
    search_fields = ['school_budget__budget_title']
