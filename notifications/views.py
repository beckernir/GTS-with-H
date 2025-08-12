from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages

from .models import Notification, UserNotification, NotificationPreference
from .forms import NotificationPreferenceForm
from core.models import User


@login_required
def notification_list(request):
    """Display user's notifications with filtering and pagination."""
    user = request.user
    
    # Get filter parameters
    status_filter = request.GET.get('status', 'all')
    type_filter = request.GET.get('type', 'all')
    priority_filter = request.GET.get('priority', 'all')
    
    # Base queryset
    notifications = UserNotification.objects.filter(
        user=user,
        is_deleted=False
    ).select_related('notification')
    
    # Apply filters
    if status_filter != 'all':
        if status_filter == 'unread':
            notifications = notifications.filter(is_read=False)
        elif status_filter == 'read':
            notifications = notifications.filter(is_read=True)
        elif status_filter == 'archived':
            notifications = notifications.filter(is_archived=True)
    
    if type_filter != 'all':
        notifications = notifications.filter(notification__notification_type=type_filter)
    
    if priority_filter != 'all':
        notifications = notifications.filter(notification__priority=priority_filter)
    
    # Pagination
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get notification counts
    unread_count = UserNotification.objects.filter(user=user, is_read=False, is_deleted=False).count()
    total_count = UserNotification.objects.filter(user=user, is_deleted=False).count()
    
    context = {
        'page_obj': page_obj,
        'unread_count': unread_count,
        'total_count': total_count,
        'status_filter': status_filter,
        'type_filter': type_filter,
        'priority_filter': priority_filter,
        'notification_types': Notification.NOTIFICATION_TYPE_CHOICES,
        'priority_choices': Notification.PRIORITY_CHOICES,
    }
    
    return render(request, 'notifications/notification_list.html', context)


@login_required
def notification_detail(request, notification_id):
    """Display detailed view of a specific notification."""
    user = request.user
    user_notification = get_object_or_404(
        UserNotification,
        user_notification_id=notification_id,
        user=user,
        is_deleted=False
    )
    
    # Mark as read if not already read
    if not user_notification.is_read:
        user_notification.mark_as_read()
    
    context = {
        'user_notification': user_notification,
        'notification': user_notification.notification,
    }
    
    return render(request, 'notifications/notification_detail.html', context)


@login_required
@require_POST
def mark_as_read(request, notification_id):
    """Mark a notification as read via AJAX."""
    user = request.user
    user_notification = get_object_or_404(
        UserNotification,
        user_notification_id=notification_id,
        user=user,
        is_deleted=False
    )
    
    user_notification.mark_as_read()
    
    return JsonResponse({
        'success': True,
        'message': 'Notification marked as read'
    })


@login_required
@require_POST
def mark_all_as_read(request):
    """Mark all user notifications as read."""
    user = request.user
    unread_notifications = UserNotification.objects.filter(
        user=user,
        is_read=False,
        is_deleted=False
    )
    
    count = unread_notifications.count()
    unread_notifications.update(
        is_read=True,
        read_at=timezone.now(),
        status='read'
    )
    
    messages.success(request, f'{count} notifications marked as read')
    return redirect('notifications:notification_list')


@login_required
@require_POST
def archive_notification(request, notification_id):
    """Archive a notification."""
    user = request.user
    user_notification = get_object_or_404(
        UserNotification,
        user_notification_id=notification_id,
        user=user,
        is_deleted=False
    )
    
    user_notification.is_archived = True
    user_notification.save()
    
    messages.success(request, 'Notification archived')
    return redirect('notifications:notification_list')


@login_required
@require_POST
def delete_notification(request, notification_id):
    """Soft delete a notification."""
    user = request.user
    user_notification = get_object_or_404(
        UserNotification,
        user_notification_id=notification_id,
        user=user,
        is_deleted=False
    )
    
    user_notification.is_deleted = True
    user_notification.save()
    
    messages.success(request, 'Notification deleted')
    return redirect('notifications:notification_list')


@login_required
def notification_preferences(request):
    """Manage user notification preferences."""
    user = request.user
    
    # Get or create preferences
    preferences, created = NotificationPreference.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form = NotificationPreferenceForm(request.POST, instance=preferences)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notification preferences updated successfully')
            return redirect('notifications:notification_preferences')
    else:
        form = NotificationPreferenceForm(instance=preferences)
    
    context = {
        'form': form,
        'preferences': preferences,
    }
    
    return render(request, 'notifications/notification_preferences.html', context)


@login_required
def notification_badge(request):
    """AJAX endpoint to get unread notification count for badge."""
    user = request.user
    unread_count = UserNotification.objects.filter(
        user=user,
        is_read=False,
        is_deleted=False
    ).count()
    
    return JsonResponse({
        'unread_count': unread_count,
        'has_notifications': unread_count > 0
    })


@login_required
def notification_dropdown(request):
    """AJAX endpoint to get recent notifications for dropdown."""
    user = request.user
    recent_notifications = UserNotification.objects.filter(
        user=user,
        is_deleted=False
    ).select_related('notification')[:5]
    
    notifications_data = []
    for user_notification in recent_notifications:
        notifications_data.append({
            'id': str(user_notification.user_notification_id),
            'title': user_notification.notification.title,
            'message': user_notification.notification.message[:100] + '...' if len(user_notification.notification.message) > 100 else user_notification.notification.message,
            'type': user_notification.notification.get_notification_type_display(),
            'priority': user_notification.notification.priority,
            'is_read': user_notification.is_read,
            'created_at': user_notification.created_at.strftime('%M minutes ago') if (timezone.now() - user_notification.created_at).seconds < 3600 else user_notification.created_at.strftime('%b %d, %Y'),
            'action_url': user_notification.notification.action_url,
        })
    
    return JsonResponse({
        'notifications': notifications_data,
        'unread_count': UserNotification.objects.filter(user=user, is_read=False, is_deleted=False).count()
    })


# Admin views for creating and managing notifications
@login_required
def admin_notification_list(request):
    """Admin view to list all system notifications."""
    if not (request.user.is_staff or request.user.is_system_admin):
        return HttpResponseForbidden()
    
    notifications = Notification.objects.all().order_by('-created_at')
    
    # Apply filters
    type_filter = request.GET.get('type', 'all')
    priority_filter = request.GET.get('priority', 'all')
    status_filter = request.GET.get('status', 'all')
    
    if type_filter != 'all':
        notifications = notifications.filter(notification_type=type_filter)
    
    if priority_filter != 'all':
        notifications = notifications.filter(priority=priority_filter)
    
    if status_filter == 'active':
        notifications = notifications.filter(is_active=True)
    elif status_filter == 'inactive':
        notifications = notifications.filter(is_active=False)
    
    # Pagination
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'type_filter': type_filter,
        'priority_filter': priority_filter,
        'status_filter': status_filter,
        'notification_types': Notification.NOTIFICATION_TYPE_CHOICES,
        'priority_choices': Notification.PRIORITY_CHOICES,
    }
    
    return render(request, 'notifications/admin_notification_list.html', context)


@login_required
def admin_notification_create(request):
    """Admin view to create new notifications."""
    if not (request.user.is_staff or request.user.is_system_admin):
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        # Handle notification creation
        title = request.POST.get('title')
        message = request.POST.get('message')
        notification_type = request.POST.get('notification_type')
        priority = request.POST.get('priority')
        target_roles = request.POST.getlist('target_roles')
        
        notification = Notification.objects.create(
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
            target_roles=target_roles,
            created_by=request.user
        )
        
        # Create UserNotification objects for target users
        target_users = User.objects.filter(role__in=target_roles)
        for user in target_users:
            UserNotification.objects.create(
                user=user,
                notification=notification
            )
        
        messages.success(request, 'Notification created and sent successfully')
        return redirect('notifications:admin_notification_list')
    
    context = {
        'notification_types': Notification.NOTIFICATION_TYPE_CHOICES,
        'priority_choices': Notification.PRIORITY_CHOICES,
        'role_choices': User.ROLE_CHOICES,
    }
    
    return render(request, 'notifications/admin_notification_create.html', context)
