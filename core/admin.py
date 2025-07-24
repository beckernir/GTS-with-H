from django.contrib import admin
from .models import AuditLog, School, SchoolUser

# Register your models here.
admin.site.register(AuditLog)
admin.site.register(School)

admin.site.site_header = 'Grant Tracker Administration'
admin.site.site_title = 'Grant Tracker Admin'
admin.site.index_title = 'Welcome to Grant Tracker Administration'

@admin.register(SchoolUser)
class SchoolUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'school_role', 'is_active', 'start_date', 'end_date')
    list_filter = ('is_active', 'school_role', 'school')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'school__school_name')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            from .models import User
            kwargs["queryset"] = User.objects.filter(role__in=['school_admin', 'teacher'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
