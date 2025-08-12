from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # User notification views
    path('', views.notification_list, name='notification_list'),
    path('detail/<uuid:notification_id>/', views.notification_detail, name='notification_detail'),
    path('mark-read/<uuid:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('mark-all-read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('archive/<uuid:notification_id>/', views.archive_notification, name='archive_notification'),
    path('delete/<uuid:notification_id>/', views.delete_notification, name='delete_notification'),
    path('preferences/', views.notification_preferences, name='notification_preferences'),
    
    # AJAX endpoints
    path('badge/', views.notification_badge, name='notification_badge'),
    path('dropdown/', views.notification_dropdown, name='notification_dropdown'),
    
    # Admin views
    path('admin/', views.admin_notification_list, name='admin_notification_list'),
    path('admin/create/', views.admin_notification_create, name='admin_notification_create'),
] 