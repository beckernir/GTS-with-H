from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    # Community overview
    path('', views.community_overview_view, name='overview'),
    
    # Community forums
    path('forums/', views.forum_list_view, name='forum_list'),
    path('forums/create/', views.forum_create_view, name='forum_create'),
    path('forums/<uuid:forum_id>/', views.forum_detail_view, name='forum_detail'),
    path('forums/<uuid:forum_id>/edit/', views.forum_edit_view, name='forum_edit'),
    
    # Forum topics
    path('forums/<uuid:forum_id>/topics/', views.topic_list_view, name='topic_list'),
    path('forums/<uuid:forum_id>/topics/create/', views.topic_create_view, name='topic_create'),
    path('topics/<uuid:topic_id>/', views.topic_detail_view, name='topic_detail'),
    path('topics/<uuid:topic_id>/edit/', views.topic_edit_view, name='topic_edit'),
    path('topics/<uuid:topic_id>/delete/', views.topic_delete_view, name='topic_delete'),
    
    # Forum posts
    path('topics/<uuid:topic_id>/posts/', views.post_list_view, name='post_list'),
    path('topics/<uuid:topic_id>/posts/create/', views.post_create_view, name='post_create'),
    path('posts/<uuid:post_id>/', views.post_detail_view, name='post_detail'),
    path('posts/<uuid:post_id>/edit/', views.post_edit_view, name='post_edit'),
    path('posts/<uuid:post_id>/delete/', views.post_delete_view, name='post_delete'),
    path('posts/<uuid:post_id>/reply/', views.post_reply_view, name='post_reply'),
    
    # Community messages
    path('messages/', views.message_list_view, name='message_list'),
    path('messages/create/', views.message_create_view, name='message_create'),
    path('messages/<uuid:message_id>/', views.message_detail_view, name='message_detail'),
    path('messages/<uuid:message_id>/reply/', views.message_reply_view, name='message_reply'),
    path('messages/<uuid:message_id>/delete/', views.message_delete_view, name='message_delete'),
    
    # Feedback
    path('feedback/', views.feedback_list_view, name='feedback_list'),
    path('feedback/create/', views.feedback_create_view, name='feedback_create'),
    path('feedback/<uuid:feedback_id>/', views.feedback_detail_view, name='feedback_detail'),
    path('feedback/<uuid:feedback_id>/edit/', views.feedback_edit_view, name='feedback_edit'),
    path('feedback/<uuid:feedback_id>/resolve/', views.feedback_resolve_view, name='feedback_resolve'),
    
    # Announcements
    path('announcements/', views.announcement_list_view, name='announcement_list'),
    path('announcements/create/', views.announcement_create_view, name='announcement_create'),
    path('announcements/<uuid:announcement_id>/', views.announcement_detail_view, name='announcement_detail'),
    path('announcements/<uuid:announcement_id>/edit/', views.announcement_edit_view, name='announcement_edit'),
    # path('announcements/<uuid:announcement_id>/acknowledge/', views.announcement_acknowledge_view, name='announcement_acknowledge'),
    
    # Community events
    path('events/', views.event_list_view, name='event_list'),
    path('events/create/', views.event_create_view, name='event_create'),
    path('events/<uuid:event_id>/', views.event_detail_view, name='event_detail'),
    path('events/<uuid:event_id>/edit/', views.event_edit_view, name='event_edit'),
    path('events/<uuid:event_id>/register/', views.event_register_view, name='event_register'),
    path('events/<uuid:event_id>/cancel/', views.event_cancel_view, name='event_cancel'),
    path('ajax/user-suggestions/', views.user_suggestions, name='user_suggestions'),
] 