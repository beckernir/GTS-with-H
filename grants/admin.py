from django.contrib import admin
from .models import GrantCategory, GrantProposal

# Register your models here.
admin.site.register(GrantCategory)

@admin.register(GrantProposal)
class GrantProposalAdmin(admin.ModelAdmin):
    list_display = ['proposal_title', 'school', 'grant_category', 'requested_amount', 'allocated_amount', 'status', 'created_at']
    list_filter = ['status', 'grant_category', 'priority_level', 'created_at']
    search_fields = ['proposal_title', 'school__school_name', 'proposal_code']
    readonly_fields = ['proposal_id', 'proposal_code', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('proposal_title', 'proposal_code', 'school', 'grant_category')
        }),
        ('Financial Information', {
            'fields': ('requested_amount', 'allocated_amount', 'disbursed_amount')
        }),
        ('Project Details', {
            'fields': ('description', 'objectives', 'expected_outcomes', 'target_beneficiaries')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'priority_level')
        }),
        ('Status', {
            'fields': ('status', 'submission_date', 'approval_date', 'completion_date')
        }),
        ('Review Information', {
            'fields': ('review_notes', 'rejection_reason')
        }),
        ('AI Scores', {
            'fields': ('ai_priority_score', 'ai_need_score', 'ai_impact_score')
        }),
        ('Audit', {
            'fields': ('created_by', 'approved_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
