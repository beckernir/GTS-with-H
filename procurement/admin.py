from django.contrib import admin
from .models import Tender, TenderDocument, TenderStatusHistory

@admin.register(Tender)
class TenderAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'submission_deadline', 'created_by', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'created_at')

@admin.register(TenderDocument)
class TenderDocumentAdmin(admin.ModelAdmin):
    list_display = ('document_title', 'tender', 'document_type', 'uploaded_by', 'uploaded_at')
    search_fields = ('document_title', 'description')
    list_filter = ('document_type', 'uploaded_at')

@admin.register(TenderStatusHistory)
class TenderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('tender', 'old_status', 'new_status', 'changed_by', 'changed_at')
    list_filter = ('old_status', 'new_status', 'changed_at')
