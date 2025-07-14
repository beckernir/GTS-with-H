from django.urls import path
from . import views

app_name = 'training'

urlpatterns = [
    # Training overview
    path('', views.training_overview_view, name='overview'),
    
    # Training categories
    path('categories/', views.category_list_view, name='category_list'),
    path('categories/<uuid:category_id>/', views.category_detail_view, name='category_detail'),
    
    # Training courses
    path('courses/', views.course_list_view, name='course_list'),
    path('courses/create/', views.course_create_view, name='course_create'),
    path('courses/<uuid:course_id>/', views.course_detail_view, name='course_detail'),
    path('courses/<uuid:course_id>/edit/', views.course_edit_view, name='course_edit'),
    
    # Course modules
    path('courses/<uuid:course_id>/modules/', views.module_list_view, name='module_list'),
    path('courses/<uuid:course_id>/modules/add/', views.module_add_view, name='module_add'),
    path('modules/<uuid:module_id>/', views.module_detail_view, name='module_detail'),
    path('modules/<uuid:module_id>/edit/', views.module_edit_view, name='module_edit'),
    path('modules/<uuid:module_id>/delete/', views.module_delete_view, name='module_delete'),
    
    # Training sessions
    path('sessions/', views.session_list_view, name='session_list'),
    path('sessions/create/', views.session_create_view, name='session_create'),
    path('sessions/<uuid:session_id>/', views.session_detail_view, name='session_detail'),
    path('sessions/<uuid:session_id>/edit/', views.session_edit_view, name='session_edit'),
    path('sessions/<uuid:session_id>/register/', views.session_register_view, name='session_register'),
    
    # Training enrollments
    path('enrollments/', views.enrollment_list_view, name='enrollment_list'),
    path('enrollments/create/', views.enrollment_create_view, name='enrollment_create'),
    path('enrollments/<uuid:enrollment_id>/', views.enrollment_detail_view, name='enrollment_detail'),
    path('enrollments/<uuid:enrollment_id>/progress/', views.enrollment_progress_view, name='enrollment_progress'),
    
    # Module progress
    path('modules/<uuid:module_id>/progress/', views.module_progress_view, name='module_progress'),
    path('modules/<uuid:module_id>/progress/update/', views.module_progress_update_view, name='module_progress_update'),
    
    # Training assessments
    path('assessments/', views.assessment_list_view, name='assessment_list'),
    path('assessments/create/', views.assessment_create_view, name='assessment_create'),
    path('assessments/<uuid:assessment_id>/', views.assessment_detail_view, name='assessment_detail'),
    path('assessments/<uuid:assessment_id>/take/', views.assessment_take_view, name='assessment_take'),
    path('assessments/<uuid:assessment_id>/submit/', views.assessment_submit_view, name='assessment_submit'),
    
    # Assessment results
    path('results/', views.result_list_view, name='result_list'),
    path('results/<uuid:result_id>/', views.result_detail_view, name='result_detail'),
    
    # Training certificates
    path('certificates/', views.certificate_list_view, name='certificate_list'),
    path('certificates/create/', views.certificate_create_view, name='certificate_create'),
    path('certificates/<uuid:certificate_id>/', views.certificate_detail_view, name='certificate_detail'),
    path('certificates/<uuid:certificate_id>/download/', views.certificate_download_view, name='certificate_download'),
    
    # Training calendar
    path('calendar/', views.calendar_view, name='calendar'),
] 