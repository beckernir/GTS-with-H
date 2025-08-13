from django.contrib import admin
from .models import GrantProposal, GrantCategory, ProposalDocument, TotalGrantAllocation

# Register your models here.
admin.site.register(GrantCategory)

@admin.register(GrantProposal)
class GrantProposalAdmin(admin.ModelAdmin):
    list_display = ['proposal_title', 'school', 'grant_category', 'effective_total_amount', 'current_amount', 'requested_amount', 'allocated_amount', 'status', 'created_at']
    list_filter = ['status', 'grant_category', 'school', 'priority_level', 'created_at']
    search_fields = ['proposal_title', 'proposal_code', 'school__school_name', 'description']
    readonly_fields = ['proposal_code', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('proposal_title', 'proposal_code', 'school', 'grant_category', 'description', 'objectives', 'expected_outcomes', 'target_beneficiaries')
        }),
        ('Financial Information', {
            'fields': ('total_amount', 'current_amount', 'requested_amount', 'allocated_amount', 'disbursed_amount')
        }),
        ('Timeline and Priority', {
            'fields': ('start_date', 'end_date', 'priority_level')
        }),
        ('Status and Workflow', {
            'fields': ('status', 'submission_date', 'approval_date', 'completion_date', 'review_notes', 'rejection_reason')
        }),
        ('AI Scores', {
            'fields': ('ai_priority_score', 'ai_need_score', 'ai_impact_score'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'approved_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def effective_total_amount(self, obj):
        """Display effective total amount (total_amount or requested_amount if total_amount is 0)."""
        return f"RWF {obj.effective_total_amount:,.2f}"
    effective_total_amount.short_description = 'Total Amount'
    effective_total_amount.admin_order_field = 'total_amount'


@admin.register(TotalGrantAllocation)
class TotalGrantAllocationAdmin(admin.ModelAdmin):
    list_display = ['fiscal_year', 'total_budget', 'allocated_amount', 'disbursed_amount', 'get_remaining_budget', 'status', 'is_active', 'created_at']
    list_filter = ['status', 'is_active', 'fiscal_year', 'created_at']
    search_fields = ['fiscal_year', 'description', 'allocation_notes']
    readonly_fields = ['allocation_id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('fiscal_year', 'total_budget', 'start_date', 'end_date')
        }),
        ('Allocation Details', {
            'fields': ('allocated_amount', 'disbursed_amount', 'status', 'is_active')
        }),
        ('Description and Notes', {
            'fields': ('description', 'allocation_notes')
        }),
        ('Metadata', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_remaining_budget(self, obj):
        """Display remaining budget."""
        remaining = obj.get_remaining_budget()
        color = 'red' if remaining < 0 else 'green'
        return f'<span style="color: {color};">RWF {remaining:,.2f}</span>'
    get_remaining_budget.short_description = 'Remaining Budget'
    get_remaining_budget.allow_tags = True
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by for new objects
            obj.created_by = request.user
        else:  # Set updated_by for existing objects
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)
