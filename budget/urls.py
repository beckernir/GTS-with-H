from django.urls import path
from . import views

app_name = 'budget'

urlpatterns = [
    # Budget overview
    path('', views.budget_overview_view, name='overview'),
    
    # Budget periods
    path('periods/', views.period_list_view, name='period_list'),
    path('periods/create/', views.period_create_view, name='period_create'),
    path('periods/<uuid:period_id>/', views.period_detail_view, name='period_detail'),
    path('periods/<uuid:period_id>/edit/', views.period_edit_view, name='period_edit'),
    path('periods/<uuid:period_id>/delete/', views.period_delete_view, name='period_delete'),
    
    # School budgets
    path('school-budgets/', views.school_budget_list_view, name='school_budget_list'),
    path('school-budgets/create/', views.school_budget_create_view, name='school_budget_create'),
    path('school-budgets/<uuid:budget_id>/', views.school_budget_detail_view, name='school_budget_detail'),
    path('school-budgets/<uuid:budget_id>/edit/', views.school_budget_edit_view, name='school_budget_edit'),
    path('school-budgets/<uuid:budget_id>/delete/', views.school_budget_delete_view, name='school_budget_delete'),
    
    # Budget categories
    path('categories/', views.category_list_view, name='category_list'),
    path('categories/<uuid:category_id>/', views.category_detail_view, name='category_detail'),
    
    # Budget line items
    path('<uuid:budget_id>/line-items/', views.line_item_list_view, name='line_item_list'),
    path('<uuid:budget_id>/line-items/add/', views.line_item_add_view, name='line_item_add'),
    path('line-items/<uuid:item_id>/', views.line_item_detail_view, name='line_item_detail'),
    path('line-items/<uuid:item_id>/edit/', views.line_item_edit_view, name='line_item_edit'),
    path('line-items/<uuid:item_id>/delete/', views.line_item_delete_view, name='line_item_delete'),
    
    # Expenditures
    path('line-items/<uuid:item_id>/expenditures/', views.expenditure_list_view, name='expenditure_list'),
    path('line-items/<uuid:item_id>/expenditures/add/', views.expenditure_add_view, name='expenditure_add'),
    path('expenditures/<uuid:expenditure_id>/', views.expenditure_detail_view, name='expenditure_detail'),
    path('expenditures/<uuid:expenditure_id>/edit/', views.expenditure_edit_view, name='expenditure_edit'),
    path('expenditures/<uuid:expenditure_id>/delete/', views.expenditure_delete_view, name='expenditure_delete'),
    
    # Budget transfers
    path('transfers/', views.transfer_list_view, name='transfer_list'),
    path('transfers/create/', views.transfer_create_view, name='transfer_create'),
    path('transfers/<uuid:transfer_id>/', views.transfer_detail_view, name='transfer_detail'),
    path('transfers/<uuid:transfer_id>/approve/', views.transfer_approve_view, name='transfer_approve'),
    
    # Budget reports
    path('reports/', views.report_list_view, name='report_list'),
    path('reports/generate/', views.report_generate_view, name='report_generate'),
    path('reports/<uuid:report_id>/', views.report_detail_view, name='report_detail'),
    path('reports/<uuid:report_id>/download/', views.report_download_view, name='report_download'),
] 