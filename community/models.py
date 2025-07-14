from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from core.models import User, School
import uuid


class CommunityForum(models.Model):
    """
    Model for community forums and discussion boards.
    """
    
    # Forum types
    FORUM_TYPE_CHOICES = [
        ('general', 'General Discussion'),
        ('grants', 'Grants Discussion'),
        ('projects', 'Project Updates'),
        ('feedback', 'Feedback and Suggestions'),
        ('announcements', 'Announcements'),
        ('help', 'Help and Support'),
        ('events', 'Events and Activities'),
        ('other', 'Other'),
    ]
    
    # Forum access levels
    ACCESS_LEVEL_CHOICES = [
        ('public', 'Public'),
        ('school_members', 'School Members Only'),
        ('registered_users', 'Registered Users Only'),
        ('moderated', 'Moderated Access'),
        ('private', 'Private'),
    ]
    
    # Core fields
    forum_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    forum_name = models.CharField(max_length=200, unique=True)
    forum_type = models.CharField(max_length=20, choices=FORUM_TYPE_CHOICES, default='general')
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVEL_CHOICES, default='public')
    
    # Forum details
    description = models.TextField()
    rules = models.TextField(blank=True, null=True)
    
    # Forum scope
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='forums', null=True, blank=True)
    
    # Forum statistics
    total_topics = models.PositiveIntegerField(default=0)
    total_posts = models.PositiveIntegerField(default=0)
    total_members = models.PositiveIntegerField(default=0)
    
    # Forum settings
    is_active = models.BooleanField(default=True)
    requires_moderation = models.BooleanField(default=False)
    allow_anonymous = models.BooleanField(default=False)
    
    # Forum moderators
    moderators = models.ManyToManyField(User, related_name='moderated_forums', blank=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_forums')
    
    class Meta:
        db_table = 'community_community_forum'
        verbose_name = 'Community Forum'
        verbose_name_plural = 'Community Forums'
        ordering = ['forum_type', 'forum_name']
    
    def __str__(self):
        return f"{self.forum_name} ({self.get_forum_type_display()})"


class ForumTopic(models.Model):
    """
    Model for topics within community forums.
    """
    
    # Topic status choices
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('locked', 'Locked'),
        ('pinned', 'Pinned'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    ]
    
    # Core fields
    topic_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    forum = models.ForeignKey(CommunityForum, on_delete=models.CASCADE, related_name='topics')
    topic_title = models.CharField(max_length=200)
    
    # Topic details
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Topic statistics
    view_count = models.PositiveIntegerField(default=0)
    reply_count = models.PositiveIntegerField(default=0)
    last_activity = models.DateTimeField(auto_now=True)
    
    # Topic settings
    is_sticky = models.BooleanField(default=False)
    is_announcement = models.BooleanField(default=False)
    allow_replies = models.BooleanField(default=True)
    
    # Topic tags
    tags = models.JSONField(default=list, help_text="JSON array of topic tags")
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_topics')
    last_post_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='last_posts_in_topics')
    
    class Meta:
        db_table = 'community_forum_topic'
        verbose_name = 'Forum Topic'
        verbose_name_plural = 'Forum Topics'
        ordering = ['-is_sticky', '-last_activity']
    
    def __str__(self):
        return f"{self.topic_title} - {self.forum.forum_name}"
    
    def get_total_posts(self):
        """Get total number of posts including the topic itself."""
        return self.reply_count + 1


class ForumPost(models.Model):
    """
    Model for posts within forum topics.
    """
    
    # Post status choices
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('hidden', 'Hidden'),
        ('deleted', 'Deleted'),
        ('moderated', 'Under Moderation'),
    ]
    
    # Core fields
    post_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE, related_name='posts')
    parent_post = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    
    # Post content
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Post statistics
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    dislike_count = models.PositiveIntegerField(default=0)
    
    # Post attachments
    attachments = models.JSONField(default=list, help_text="JSON array of attachment file paths")
    
    # Post moderation
    is_edited = models.BooleanField(default=False)
    edit_reason = models.TextField(blank=True, null=True)
    moderation_notes = models.TextField(blank=True, null=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_posts')
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='edited_posts')
    
    class Meta:
        db_table = 'community_forum_post'
        verbose_name = 'Forum Post'
        verbose_name_plural = 'Forum Posts'
        ordering = ['topic', 'created_at']
    
    def __str__(self):
        return f"Post by {self.created_by.get_full_name()} in {self.topic.topic_title}"
    
    def get_reply_count(self):
        """Get number of direct replies to this post."""
        return self.replies.count()


class CommunityMessage(models.Model):
    """
    Model for direct messages between community members.
    """
    
    # Message types
    MESSAGE_TYPE_CHOICES = [
        ('direct', 'Direct Message'),
        ('group', 'Group Message'),
        ('announcement', 'Announcement'),
        ('notification', 'Notification'),
        ('system', 'System Message'),
    ]
    
    # Message status choices
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    ]
    
    # Core fields
    message_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='direct')
    subject = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField()
    
    # Message participants
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipients = models.ManyToManyField(User, related_name='received_messages')
    
    # Message scope
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    
    # Message status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    is_urgent = models.BooleanField(default=False)
    requires_confirmation = models.BooleanField(default=False)
    
    # Message attachments
    attachments = models.JSONField(default=list, help_text="JSON array of attachment file paths")
    
    # Message tracking
    read_at = models.DateTimeField(blank=True, null=True)
    replied_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'community_community_message'
        verbose_name = 'Community Message'
        verbose_name_plural = 'Community Messages'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.sender.get_full_name()} - {self.subject or 'No Subject'}"


class Feedback(models.Model):
    """
    Model for community feedback and suggestions.
    """
    
    # Feedback types
    FEEDBACK_TYPE_CHOICES = [
        ('suggestion', 'Suggestion'),
        ('complaint', 'Complaint'),
        ('compliment', 'Compliment'),
        ('bug_report', 'Bug Report'),
        ('feature_request', 'Feature Request'),
        ('general', 'General Feedback'),
    ]
    
    # Feedback priority levels
    PRIORITY_CHOICES = [
        ('low', 'Low Priority'),
        ('medium', 'Medium Priority'),
        ('high', 'High Priority'),
        ('urgent', 'Urgent'),
    ]
    
    # Feedback status choices
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
        ('closed', 'Closed'),
    ]
    
    # Core fields
    feedback_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPE_CHOICES, default='general')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    
    # Feedback content
    title = models.CharField(max_length=200)
    description = models.TextField()
    suggestions = models.TextField(blank=True, null=True)
    
    # Feedback scope
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='feedback', null=True, blank=True)
    related_module = models.CharField(max_length=50, blank=True, null=True, help_text="Related system module")
    
    # Feedback tracking
    submission_date = models.DateTimeField(auto_now_add=True)
    review_date = models.DateTimeField(blank=True, null=True)
    resolution_date = models.DateTimeField(blank=True, null=True)
    
    # Feedback response
    response = models.TextField(blank=True, null=True)
    resolution_notes = models.TextField(blank=True, null=True)
    
    # Feedback attachments
    attachments = models.JSONField(default=list, help_text="JSON array of attachment file paths")
    
    # Feedback metrics
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_feedback')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_feedback')
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_feedback')
    
    class Meta:
        db_table = 'community_feedback'
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback'
        ordering = ['-priority', '-submission_date']
    
    def __str__(self):
        return f"{self.title} - {self.get_feedback_type_display()}"


class Announcement(models.Model):
    """
    Model for system announcements and notifications.
    """
    
    # Announcement types
    ANNOUNCEMENT_TYPE_CHOICES = [
        ('general', 'General Announcement'),
        ('grant_related', 'Grant Related'),
        ('training', 'Training Announcement'),
        ('maintenance', 'System Maintenance'),
        ('security', 'Security Notice'),
        ('event', 'Event Announcement'),
        ('urgent', 'Urgent Notice'),
    ]
    
    # Announcement priority levels
    PRIORITY_CHOICES = [
        ('low', 'Low Priority'),
        ('normal', 'Normal Priority'),
        ('high', 'High Priority'),
        ('urgent', 'Urgent'),
    ]
    
    # Core fields
    announcement_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    announcement_type = models.CharField(max_length=20, choices=ANNOUNCEMENT_TYPE_CHOICES, default='general')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    
    # Announcement content
    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.TextField(blank=True, null=True)
    
    # Announcement scope
    target_audience = models.JSONField(default=list, help_text="JSON array of target user roles")
    target_schools = models.ManyToManyField(School, related_name='announcements', blank=True)
    
    # Announcement scheduling
    publish_date = models.DateTimeField()
    expiry_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # Announcement settings
    requires_acknowledgment = models.BooleanField(default=False)
    show_on_dashboard = models.BooleanField(default=True)
    send_email_notification = models.BooleanField(default=False)
    
    # Announcement attachments
    attachments = models.JSONField(default=list, help_text="JSON array of attachment file paths")
    
    # Announcement tracking
    view_count = models.PositiveIntegerField(default=0)
    acknowledgment_count = models.PositiveIntegerField(default=0)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_announcements')
    
    class Meta:
        db_table = 'community_announcement'
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
        ordering = ['-priority', '-publish_date']
    
    def __str__(self):
        return f"{self.title} - {self.get_announcement_type_display()}"
    
    def is_expired(self):
        """Check if announcement has expired."""
        if self.expiry_date:
            return timezone.now() > self.expiry_date
        return False
    
    def is_published(self):
        """Check if announcement is published."""
        return timezone.now() >= self.publish_date


class CommunityEvent(models.Model):
    """
    Model for community events and activities.
    """
    
    # Event types
    EVENT_TYPE_CHOICES = [
        ('meeting', 'Meeting'),
        ('workshop', 'Workshop'),
        ('training', 'Training Session'),
        ('conference', 'Conference'),
        ('celebration', 'Celebration'),
        ('awareness', 'Awareness Campaign'),
        ('other', 'Other'),
    ]
    
    # Event status choices
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('registration_open', 'Registration Open'),
        ('registration_closed', 'Registration Closed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Core fields
    event_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='other')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Event details
    event_title = models.CharField(max_length=200)
    description = models.TextField()
    objectives = models.TextField(blank=True, null=True)
    
    # Event scheduling
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_deadline = models.DateTimeField(blank=True, null=True)
    
    # Event location
    location = models.CharField(max_length=200, blank=True, null=True)
    is_virtual = models.BooleanField(default=False)
    virtual_meeting_link = models.URLField(blank=True, null=True)
    
    # Event capacity
    max_participants = models.PositiveIntegerField(default=0, help_text="0 for unlimited")
    current_participants = models.PositiveIntegerField(default=0)
    
    # Event organizers
    organizers = models.ManyToManyField(User, related_name='organized_events')
    contact_person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='contact_for_events')
    
    # Event scope
    target_audience = models.JSONField(default=list, help_text="JSON array of target user roles")
    target_schools = models.ManyToManyField(School, related_name='events', blank=True)
    
    # Event materials
    event_materials = models.JSONField(default=list, help_text="JSON array of event material file paths")
    
    # Event tracking
    view_count = models.PositiveIntegerField(default=0)
    registration_count = models.PositiveIntegerField(default=0)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    
    class Meta:
        db_table = 'community_community_event'
        verbose_name = 'Community Event'
        verbose_name_plural = 'Community Events'
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.event_title} - {self.get_event_type_display()}"
    
    def get_duration_hours(self):
        """Calculate event duration in hours."""
        duration = self.end_date - self.start_date
        return duration.total_seconds() / 3600
    
    def is_registration_open(self):
        """Check if event registration is open."""
        if not self.registration_deadline:
            return self.status == 'registration_open'
        return self.status == 'registration_open' and timezone.now() <= self.registration_deadline
    
    def get_available_slots(self):
        """Get number of available slots."""
        if self.max_participants == 0:
            return float('inf')
        return max(0, self.max_participants - self.current_participants)
