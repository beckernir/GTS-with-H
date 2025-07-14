from django.urls import path
from . import views

app_name = 'grants'

urlpatterns = [
    # Grant proposals
    path('', views.proposal_list_view, name='proposal_list'),
    path('create/', views.proposal_create_view, name='proposal_create'),
    path('<uuid:proposal_id>/', views.proposal_detail_view, name='proposal_detail'),
    path('<uuid:proposal_id>/edit/', views.proposal_edit_view, name='proposal_edit'),
    path('<uuid:proposal_id>/submit/', views.proposal_submit_view, name='proposal_submit'),
    path('<uuid:proposal_id>/delete/', views.proposal_delete_view, name='proposal_delete'),
    path('<uuid:proposal_id>/approve/', views.proposal_approve_view, name='proposal_approve'),
    path('<uuid:proposal_id>/reject/', views.proposal_reject_view, name='proposal_reject'),
    path('<uuid:proposal_id>/allocate/', views.proposal_allocate_view, name='proposal_allocate'),
    
    # Grant categories
    path('categories/', views.category_list_view, name='category_list'),
    path('categories/create/', views.category_create_view, name='category_create'),
    path('categories/<uuid:category_id>/edit/', views.category_edit_view, name='category_edit'),
    path('categories/<uuid:category_id>/delete/', views.category_delete_view, name='category_delete'),
    path('categories/<uuid:category_id>/', views.category_detail_view, name='category_detail'),
    path('categories/export/excel/', views.category_export_excel_view, name='category_export_excel'),
    path('categories/export/pdf/', views.category_export_pdf_view, name='category_export_pdf'),
    
    # Proposal documents
    path('<uuid:proposal_id>/documents/', views.document_list_view, name='document_list'),
    path('<uuid:proposal_id>/documents/upload/', views.document_upload_view, name='document_upload'),
    path('documents/<uuid:document_id>/', views.document_detail_view, name='document_detail'),
    path('documents/<uuid:document_id>/delete/', views.document_delete_view, name='document_delete'),
    
    # Budget management
    path('<uuid:proposal_id>/budget/', views.budget_view, name='budget'),
    path('<uuid:proposal_id>/budget/add/', views.budget_item_add_view, name='budget_item_add'),
    path('<uuid:proposal_id>/budget/<uuid:item_id>/edit/', views.budget_item_edit_view, name='budget_item_edit'),
    path('<uuid:proposal_id>/budget/<uuid:item_id>/delete/', views.budget_item_delete_view, name='budget_item_delete'),
    
    # Fund allocation
    path('<uuid:proposal_id>/allocation/', views.allocation_view, name='allocation'),
    path('<uuid:proposal_id>/allocation/create/', views.allocation_create_view, name='allocation_create'),
    
    # Proposal review
    path('<uuid:proposal_id>/review/', views.proposal_review_view, name='proposal_review'),
    path('<uuid:proposal_id>/review/create/', views.review_create_view, name='review_create'),
    
    # AI allocation
    path('ai-allocation/', views.ai_allocation_view, name='ai_allocation'),
    path('ai-allocation/run/', views.ai_allocation_run_view, name='ai_allocation_run'),

    # Enrollment
    # path('enrollments/', views.enrollment_list_view, name='enrollment_list'),
    # path('enrollments/create/', views.enrollment_create, name='enrollment_create'),
    # path('enrollments/<int:enrollment_id>/', views.enrollment_detail, name='enrollment_detail'),
    # path('enrollments/<int:enrollment_id>/edit/', views.enrollment_edit, name='enrollment_edit'),
] 