from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import AuditLog, School, SchoolUser, User

# Register your models here.
admin.site.register(AuditLog)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Enhanced User admin with school assignment functionality."""
    
    list_display = ('username', 'email', 'full_name', 'role', 'status', 'school_assignments', 'created_at')
    list_filter = ('role', 'status', 'created_at', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Information', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'profile_picture', 'date_of_birth', 'address', 'emergency_contact')}),
        ('Role & Status', {'fields': ('role', 'status')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'role', 'status'),
        }),
    )
    
    readonly_fields = ('user_id', 'created_at', 'updated_at', 'last_login_ip')
    
    def full_name(self, obj):
        return obj.get_full_name()
    full_name.short_description = 'Full Name'
    
    def school_assignments(self, obj):
        """Display school assignments with links to manage them."""
        assignments = SchoolUser.objects.filter(user=obj, is_active=True)
        if not assignments:
            return "No schools assigned"
        
        links = []
        for assignment in assignments:
            school_url = reverse('admin:core_school_change', args=[assignment.school.id])
            assignment_url = reverse('admin:core_schooluser_change', args=[assignment.id])
            links.append(
                f'<a href="{school_url}">{assignment.school.school_name}</a> '
                f'(<a href="{assignment_url}">Edit Assignment</a>)'
            )
        
        return mark_safe('<br>'.join(links))
    school_assignments.short_description = 'School Assignments'
    
    def get_queryset(self, request):
        """Optimize queryset with related school assignments."""
        return super().get_queryset(request).prefetch_related('school_assignments__school')
    
    actions = ['activate_users', 'deactivate_users', 'assign_school_role']
    
    def activate_users(self, request, queryset):
        """Bulk activate users."""
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} users were successfully activated.')
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        """Bulk deactivate users."""
        updated = queryset.update(status='inactive')
        self.message_user(request, f'{updated} users were successfully deactivated.')
    deactivate_users.short_description = "Deactivate selected users"
    
    def assign_school_role(self, request, queryset):
        """Bulk assign school role to users."""
        # This would redirect to a custom admin action page
        pass
    assign_school_role.short_description = "Assign schools to selected users"

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    """Enhanced School admin."""
    
    list_display = ('school_name', 'school_code', 'district', 'level', 'total_students', 'status', 'created_at')
    list_filter = ('status', 'level', 'district', 'created_at')
    search_fields = ('school_name', 'school_code', 'district', 'sector')
    ordering = ('school_name',)
    
    fieldsets = (
        ('Basic Information', {'fields': ('school_name', 'school_code', 'level', 'status')}),
        ('Location', {'fields': ('district', 'sector', 'cell', 'village', 'address', 'latitude', 'longitude')}),
        ('Statistics', {'fields': ('total_students', 'total_teachers', 'total_staff')}),
        ('Contact Information', {'fields': ('phone_number', 'email_address', 'website')}),
        ('Leadership', {'fields': ('principal_name', 'principal_phone', 'principal_email')}),
        ('Performance Metrics', {'fields': ('academic_performance_score', 'infrastructure_score', 'need_score')}),
        ('System Information', {'fields': ('created_by', 'created_at', 'updated_at')}),
    )
    
    readonly_fields = ('school_id', 'created_at', 'updated_at')
    
    def get_queryset(self, request):
        """Optimize queryset with related data."""
        return super().get_queryset(request).select_related('created_by')

@admin.register(SchoolUser)
class SchoolUserAdmin(admin.ModelAdmin):
    """Enhanced SchoolUser admin for managing school assignments."""
    
    list_display = ('user', 'school', 'school_role', 'is_active', 'start_date', 'end_date', 'permissions_summary', 'assigned_by')
    list_filter = ('is_active', 'school_role', 'school', 'start_date', 'assigned_by')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'school__school_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Assignment Details', {'fields': ('user', 'school', 'school_role')}),
        ('Timeline', {'fields': ('start_date', 'end_date', 'is_active')}),
        ('Permissions', {'fields': ('can_submit_proposals', 'can_manage_budget', 'can_view_reports', 'can_manage_users')}),
        ('System Information', {'fields': ('assigned_by', 'created_at', 'updated_at')}),
    )
    
    readonly_fields = ('assigned_by', 'created_at', 'updated_at')
    
    def permissions_summary(self, obj):
        """Display a summary of permissions."""
        permissions = []
        if obj.can_submit_proposals:
            permissions.append('Proposals')
        if obj.can_manage_budget:
            permissions.append('Budget')
        if obj.can_view_reports:
            permissions.append('Reports')
        if obj.can_manage_users:
            permissions.append('Users')
        
        if not permissions:
            return "No permissions"
        
        return ', '.join(permissions)
    permissions_summary.short_description = 'Permissions'
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter users and schools based on context."""
        if db_field.name == "user":
            # Only show users who can be assigned to schools
            kwargs["queryset"] = User.objects.filter(role__in=['school_admin', 'teacher'])
        elif db_field.name == "school":
            # Only show active schools
            kwargs["queryset"] = School.objects.filter(status='active')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        """Automatically set assigned_by field."""
        if not change:  # Only for new assignments
            obj.assigned_by = request.user
        super().save_model(request, obj, form, change)
    
    actions = ['activate_assignments', 'deactivate_assignments']
    
    def activate_assignments(self, request, queryset):
        """Bulk activate school assignments."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} school assignments were successfully activated.')
    activate_assignments.short_description = "Activate selected assignments"
    
    def deactivate_assignments(self, request, queryset):
        """Bulk deactivate school assignments."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} school assignments were successfully deactivated.')
    deactivate_assignments.short_description = "Deactivate selected assignments"

# Admin site configuration
admin.site.site_header = 'Grant Tracker Administration'
admin.site.site_title = 'Grant Tracker Admin'
admin.site.index_title = 'Welcome to Grant Tracker Administration'
