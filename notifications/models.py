from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from core.models import School
import uuid

User = get_user_model()


class Notification(models.Model):
    """System-wide notifications that can be sent to multiple users."""
    
    NOTIFICATION_TYPE_CHOICES = [
        ('grant_proposal', 'Grant Proposal'),
        ('budget_allocation', 'Budget Allocation'),
        ('training_enrollment', 'Training Enrollment'),
        ('system_alert', 'System Alert'),
        ('approval_request', 'Approval Request'),
        ('reminder', 'Reminder'),
        ('announcement', 'Announcement'),
        ('custom', 'Custom'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    notification_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, default='custom')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    summary = models.TextField(blank=True, null=True)
    
    target_roles = models.JSONField(default=list, help_text="List of target user roles")
    target_schools = models.ManyToManyField(School, related_name='notifications', blank=True)
    target_users = models.ManyToManyField(User, related_name='direct_notifications', blank=True)
    
    requires_action = models.BooleanField(default=False)
    action_url = models.URLField(blank=True, null=True)
    action_text = models.CharField(max_length=50, blank=True, null=True)
    
    scheduled_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    send_email = models.BooleanField(default=False)
    send_sms = models.BooleanField(default=False)
    
    related_object_type = models.CharField(max_length=50, blank=True, null=True)
    related_object_id = models.CharField(max_length=50, blank=True, null=True)
    metadata = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_notifications')
    
    class Meta:
        db_table = 'notifications_notification'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_notification_type_display()})"
    
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    def should_send_now(self):
        if not self.is_active or self.is_expired():
            return False
        if self.scheduled_at and timezone.now() < self.scheduled_at:
            return False
        return True


class UserNotification(models.Model):
    """Individual user notifications with read status."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
        ('failed', 'Failed'),
    ]
    
    user_notification_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notifications')
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='user_notifications')
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    read_at = models.DateTimeField(blank=True, null=True)
    
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    
    action_taken = models.BooleanField(default=False)
    action_taken_at = models.DateTimeField(blank=True, null=True)
    
    email_sent = models.BooleanField(default=False)
    sms_sent = models.BooleanField(default=False)
    
    delivery_error = models.TextField(blank=True, null=True)
    retry_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notifications_user_notification'
        ordering = ['-created_at']
        unique_together = ['user', 'notification']
    
    def __str__(self):
        return f"{self.user.username} - {self.notification.title}"
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.status = 'read'
            self.save()
    
    def mark_as_delivered(self):
        if self.status == 'sent':
            self.status = 'delivered'
            self.delivered_at = timezone.now()
            self.save()


class NotificationPreference(models.Model):
    """User preferences for notification delivery."""
    
    FREQUENCY_CHOICES = [
        ('immediate', 'Immediate'),
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('never', 'Never'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    in_app_notifications = models.BooleanField(default=True)
    
    email_frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='immediate')
    sms_frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='never')
    
    grant_notifications = models.BooleanField(default=True)
    budget_notifications = models.BooleanField(default=True)
    training_notifications = models.BooleanField(default=True)
    system_notifications = models.BooleanField(default=True)
    
    quiet_hours_enabled = models.BooleanField(default=False)
    quiet_hours_start = models.TimeField(blank=True, null=True)
    quiet_hours_end = models.TimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notifications_preference'
    
    def __str__(self):
        return f"Preferences for {self.user.username}"
    
    def is_quiet_hours(self):
        if not self.quiet_hours_enabled:
            return False
        if not self.quiet_hours_start or not self.quiet_hours_end:
            return False
        current_time = timezone.now().time()
        return self.quiet_hours_start <= current_time <= self.quiet_hours_end
