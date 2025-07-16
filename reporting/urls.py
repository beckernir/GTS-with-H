from django.urls import path
from . import views

app_name = 'reporting'

urlpatterns = [
    # Dashboards
    path('', views.dashboard_overview_view, name='overview'),
    path('dashboards/', views.dashboard_list_view, name='dashboard_list'),
    path('dashboards/create/', views.dashboard_create_view, name='dashboard_create'),
    path('dashboards/<uuid:dashboard_id>/', views.dashboard_detail_view, name='dashboard_detail'),
    path('dashboards/<uuid:dashboard_id>/edit/', views.dashboard_edit_view, name='dashboard_edit'),
    
    # Dashboard widgets
    path('dashboards/<uuid:dashboard_id>/widgets/', views.widget_list_view, name='widget_list'),
    path('dashboards/<uuid:dashboard_id>/widgets/add/', views.widget_add_view, name='widget_add'),
    path('widgets/<uuid:widget_id>/', views.widget_detail_view, name='widget_detail'),
    path('widgets/<uuid:widget_id>/edit/', views.widget_edit_view, name='widget_edit'),
    path('widgets/<uuid:widget_id>/delete/', views.widget_delete_view, name='widget_delete'),
    
    # KPIs
    path('kpis/', views.kpi_list_view, name='kpi_list'),
    path('kpis/create/', views.kpi_create_view, name='kpi_create'),
    path('kpis/<uuid:kpi_id>/', views.kpi_detail_view, name='kpi_detail'),
    path('kpis/<uuid:kpi_id>/edit/', views.kpi_edit_view, name='kpi_edit'),
    path('kpis/<uuid:kpi_id>/values/', views.kpi_values_view, name='kpi_values'),
    
    # Reports
    path('reports/', views.report_list_view, name='report_list'),
    path('reports/create/', views.report_create_view, name='report_create'),
    path('reports/<uuid:report_id>/', views.report_detail_view, name='report_detail'),
    path('reports/<uuid:report_id>/generate/', views.report_generate_view, name='report_generate'),
    path('reports/<uuid:report_id>/download/', views.report_download_view, name='report_download'),
    
    # Report schedules
    path('schedules/', views.schedule_list_view, name='schedule_list'),
    path('schedules/create/', views.schedule_create_view, name='schedule_create'),
    path('schedules/<uuid:schedule_id>/', views.schedule_detail_view, name='schedule_detail'),
    path('schedules/<uuid:schedule_id>/edit/', views.schedule_edit_view, name='schedule_edit'),
    
    # Analytics
    path('analytics/', views.analytics_overview_view, name='analytics_overview'),
    path('analytics/events/', views.analytics_events_view, name='analytics_events'),
    path('analytics/users/', views.analytics_users_view, name='analytics_users'),
    path('analytics/performance/', views.analytics_performance_view, name='analytics_performance'),
    
    # Data exports
    path('exports/', views.export_list_view, name='export_list'),
    path('exports/create/', views.export_create_view, name='export_create'),
    path('exports/<uuid:export_id>/', views.export_detail_view, name='export_detail'),
    path('exports/<uuid:export_id>/download/', views.export_download_view, name='export_download'),
    
    # Report template generation
    path('generate/<str:template_type>/', views.generate_template_report, name='report_generate'),
    path('school-grant-totals/', views.school_grant_totals_view, name='school_grant_totals'),
    path('annual/', views.annual_grant_report_view, name='annual_grant_report'),
    path('annual/export/<str:format>/', views.annual_grant_report_export_view, name='annual_grant_report_export'),
]

urlpatterns += [
    path('reb-budget-planning/', views.reb_budget_planning_view, name='reb_budget_planning'),
    path('reb-budget-planning/edit/', views.reb_budget_edit_view, name='reb_budget_edit'),
    path('reb-budget-planning/export/excel/', views.reb_budget_planning_export_excel, name='reb_budget_planning_export_excel'),
    path('reb-budget-planning/export/pdf/', views.reb_budget_planning_export_pdf, name='reb_budget_planning_export_pdf'),
] 