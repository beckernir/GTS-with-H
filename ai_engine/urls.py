from django.urls import path
from . import views

app_name = 'ai_engine'

urlpatterns = [
    # AI Engine overview
    path('', views.ai_overview_view, name='overview'),
    
    # Allocation algorithms
    path('algorithms/', views.algorithm_list_view, name='algorithm_list'),
    path('algorithms/create/', views.algorithm_create_view, name='algorithm_create'),
    path('algorithms/<uuid:algorithm_id>/', views.algorithm_detail_view, name='algorithm_detail'),
    path('algorithms/<uuid:algorithm_id>/edit/', views.algorithm_edit_view, name='algorithm_edit'),
    path('algorithms/<uuid:algorithm_id>/test/', views.algorithm_test_view, name='algorithm_test'),
    
    # Allocation factors
    path('factors/', views.factor_list_view, name='factor_list'),
    path('factors/create/', views.factor_create_view, name='factor_create'),
    path('factors/<uuid:factor_id>/', views.factor_detail_view, name='factor_detail'),
    path('factors/<uuid:factor_id>/edit/', views.factor_edit_view, name='factor_edit'),
    
    # Allocation runs
    path('runs/', views.run_list_view, name='run_list'),
    path('runs/create/', views.run_create_view, name='run_create'),
    path('runs/<uuid:run_id>/', views.run_detail_view, name='run_detail'),
    path('runs/<uuid:run_id>/execute/', views.run_execute_view, name='run_execute'),
    path('runs/<uuid:run_id>/cancel/', views.run_cancel_view, name='run_cancel'),
    
    # Proposal allocation scores
    path('scores/', views.score_list_view, name='score_list'),
    path('scores/<uuid:score_id>/', views.score_detail_view, name='score_detail'),
    
    # Risk assessment
    path('risks/', views.risk_list_view, name='risk_list'),
    path('risks/create/', views.risk_create_view, name='risk_create'),
    path('risks/<uuid:risk_id>/', views.risk_detail_view, name='risk_detail'),
    path('risks/<uuid:risk_id>/edit/', views.risk_edit_view, name='risk_edit'),
    path('risks/<uuid:risk_id>/resolve/', views.risk_resolve_view, name='risk_resolve'),
    
    # Optimization recommendations
    path('recommendations/', views.recommendation_list_view, name='recommendation_list'),
    path('recommendations/create/', views.recommendation_create_view, name='recommendation_create'),
    path('recommendations/<uuid:recommendation_id>/', views.recommendation_detail_view, name='recommendation_detail'),
    path('recommendations/<uuid:recommendation_id>/implement/', views.recommendation_implement_view, name='recommendation_implement'),
    
    # Performance metrics
    path('metrics/', views.metric_list_view, name='metric_list'),
    path('metrics/create/', views.metric_create_view, name='metric_create'),
    path('metrics/<uuid:metric_id>/', views.metric_detail_view, name='metric_detail'),
    path('metrics/<uuid:metric_id>/edit/', views.metric_edit_view, name='metric_edit'),
    
    # AI configuration
    path('config/', views.config_view, name='config'),
    path('config/update/', views.config_update_view, name='config_update'),
] 