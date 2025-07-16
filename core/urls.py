from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Home page
    path('', views.home_view, name='home'),
    # Authentication views
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('register/supplier/', views.supplier_register_view, name='supplier_register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    
    # Dashboard views
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/<str:role>/', views.role_dashboard_view, name='role_dashboard'),
    
    # School management
    path('schools/add/', views.school_create_view, name='school_add'),
    path('schools/', views.school_list_view, name='school_list'),
    path('schools/<uuid:school_id>/', views.school_detail_view, name='school_detail'),
    path('schools/<uuid:school_id>/edit/', views.school_edit_view, name='school_edit'),
    
    # User management
    path('users/', views.user_list_view, name='user_list'),
    path('users/<uuid:user_id>/', views.user_detail_view, name='user_detail'),
    path('users/<uuid:user_id>/edit/', views.user_edit_view, name='user_edit'),
    path('users/<uuid:user_id>/activate/', views.user_activate_view, name='user_activate'),
    path('users/<uuid:user_id>/deactivate/', views.user_deactivate_view, name='user_deactivate'),
    path('users/<uuid:user_id>/delete/', views.user_delete_view, name='user_delete'),
    path('users/add/', views.user_create_view, name='user_add'),
    
    # System configuration
    path('settings/', views.settings_view, name='settings'),
    path('settings/system/', views.system_settings_view, name='system_settings'),
    
    # Error pages
    path('404/', views.custom_404, name='404'),
    path('500/', views.custom_500, name='500'),
] 