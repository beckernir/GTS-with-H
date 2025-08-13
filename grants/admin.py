from django.contrib import admin
from .models import GrantProposal, GrantCategory, ProposalDocument

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
