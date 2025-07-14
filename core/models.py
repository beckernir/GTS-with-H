from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid
from django.conf import settings


class User(AbstractUser):
    """
    Extended User model with role-based access control for GrantTracker system.
    Supports REB Officers, School Admins, Teachers, and Community Members.
    """
    
    # User role choices
    ROLE_CHOICES = [
        ('reb_officer', 'REB Officer'),
        ('school_admin', 'School Administrator'),
        ('teacher', 'Teacher'),
        ('community_member', 'Community Member'),
        ('system_admin', 'System Administrator'),
    ]
    
    # User status choices
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('pending', 'Pending Approval'),
    ]
    
    # Core user fields
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='teacher')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    # Additional fields for user management
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    
    class Meta:
        db_table = 'core_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def get_role_display_name(self):
        """Get human-readable role name."""
        return dict(self.ROLE_CHOICES).get(self.role, self.role)
    
    def is_reb_officer(self):
        """Check if user is an REB officer."""
        return self.role == 'reb_officer'
    
    def is_school_admin(self):
        """Check if user is a school administrator."""
        return self.role == 'school_admin'
    
    def is_teacher(self):
        """Check if user is a teacher."""
        return self.role == 'teacher'
    
    def is_community_member(self):
        """Check if user is a community member."""
        return self.role == 'community_member'
    
    def is_system_admin(self):
        """Check if user is a system administrator."""
        return self.role == 'system_admin'


class School(models.Model):
    """
    Model representing government secondary schools in Rwanda.
    Each school can have multiple users and grant proposals.
    """
    
    # School status choices
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    
    # School level choices
    LEVEL_CHOICES = [
        ('lower_secondary', 'Lower Secondary (S1-S3)'),
        ('upper_secondary', 'Upper Secondary (S4-S6)'),
        ('both', 'Both Lower and Upper Secondary'),
    ]
    
    # Core school fields
    school_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    school_name = models.CharField(max_length=200, unique=True)
    school_code = models.CharField(max_length=20, unique=True, help_text="Official REB school code")
    district = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    cell = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    
    # School details
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='both')
    total_students = models.PositiveIntegerField(default=0)
    total_teachers = models.PositiveIntegerField(default=0)
    total_staff = models.PositiveIntegerField(default=0)
    
    # Contact information
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    # Physical address
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    # School status and management
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    principal_name = models.CharField(max_length=100, blank=True, null=True)
    principal_phone = models.CharField(max_length=15, blank=True, null=True)
    principal_email = models.EmailField(blank=True, null=True)
    
    # Performance metrics (for AI allocation)
    academic_performance_score = models.DecimalField(
        max_digits=5, decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0.00,
        help_text="Academic performance score (0-100)"
    )
    infrastructure_score = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0.00,
        help_text="Infrastructure quality score (0-100)"
    )
    need_score = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0.00,
        help_text="Need assessment score (0-100)"
    )
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_schools')
    
    class Meta:
        db_table = 'core_school'
        verbose_name = 'School'
        verbose_name_plural = 'Schools'
        ordering = ['school_name']
    
    def __str__(self):
        return f"{self.school_name} ({self.school_code})"
    
    def get_full_address(self):
        """Get complete school address."""
        return f"{self.address}, {self.village}, {self.cell}, {self.sector}, {self.district}"
    
    def get_total_enrollment(self):
        """Get total student enrollment."""
        return self.total_students
    
    def get_performance_index(self):
        """Calculate overall performance index for AI allocation."""
        return (self.academic_performance_score + self.infrastructure_score + self.need_score) / 3


class SchoolUser(models.Model):
    """
    Junction table linking users to schools with specific roles and permissions.
    """
    
    # User role at school choices
    SCHOOL_ROLE_CHOICES = [
        ('principal', 'Principal'),
        ('deputy_principal', 'Deputy Principal'),
        ('head_teacher', 'Head Teacher'),
        ('teacher', 'Teacher'),
        ('admin_staff', 'Administrative Staff'),
        ('support_staff', 'Support Staff'),
    ]
    
    # Core relationship fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='school_assignments')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='user_assignments')
    school_role = models.CharField(max_length=20, choices=SCHOOL_ROLE_CHOICES, default='teacher')
    
    # Assignment details
    is_active = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    
    # Permissions and access
    can_submit_proposals = models.BooleanField(default=False)
    can_manage_budget = models.BooleanField(default=False)
    can_view_reports = models.BooleanField(default=True)
    can_manage_users = models.BooleanField(default=False)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_school_users')
    
    class Meta:
        db_table = 'core_school_user'
        verbose_name = 'School User Assignment'
        verbose_name_plural = 'School User Assignments'
        unique_together = ['user', 'school']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.school.school_name} ({self.get_school_role_display()})"
    
    def is_current_assignment(self):
        """Check if this is the current active assignment."""
        today = timezone.now().date()
        return (self.is_active and 
                self.start_date <= today and 
                (self.end_date is None or self.end_date >= today))


class District(models.Model):
    """
    Model representing districts in Rwanda for geographical organization.
    """
    
    district_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    district_name = models.CharField(max_length=100, unique=True)
    district_code = models.CharField(max_length=10, unique=True)
    province = models.CharField(max_length=100)
    
    # District statistics
    total_schools = models.PositiveIntegerField(default=0)
    total_students = models.PositiveIntegerField(default=0)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'core_district'
        verbose_name = 'District'
        verbose_name_plural = 'Districts'
        ordering = ['district_name']
    
    def __str__(self):
        return f"{self.district_name} ({self.province})"


class SystemConfiguration(models.Model):
    """
    Model for storing system-wide configuration settings.
    """
    
    # Configuration categories
    CATEGORY_CHOICES = [
        ('ai_allocation', 'AI Allocation Engine'),
        ('grant_limits', 'Grant Limits and Rules'),
        ('reporting', 'Reporting Settings'),
        ('notifications', 'Notification Settings'),
        ('security', 'Security Settings'),
        ('general', 'General Settings'),
    ]
    
    # Core fields
    config_key = models.CharField(max_length=100, unique=True)
    config_value = models.TextField()
    config_type = models.CharField(max_length=20, default='string')  # string, integer, float, boolean, json
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    description = models.TextField(blank=True, null=True)
    
    # Configuration metadata
    is_active = models.BooleanField(default=True)
    is_system = models.BooleanField(default=False, help_text="System configurations cannot be modified by users")
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_configs')
    
    class Meta:
        db_table = 'core_system_configuration'
        verbose_name = 'System Configuration'
        verbose_name_plural = 'System Configurations'
        ordering = ['category', 'config_key']
    
    def __str__(self):
        return f"{self.config_key} ({self.category})"
    
    def get_value(self):
        """Get typed configuration value."""
        if self.config_type == 'integer':
            return int(self.config_value)
        elif self.config_type == 'float':
            return float(self.config_value)
        elif self.config_type == 'boolean':
            return self.config_value.lower() in ('true', '1', 'yes')
        elif self.config_type == 'json':
            import json
            return json.loads(self.config_value)
        else:
            return self.config_value


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    object_type = models.CharField(max_length=50)
    object_id = models.CharField(max_length=50)
    object_repr = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.timestamp} - {self.user} - {self.action} {self.object_type} ({self.object_id})"
