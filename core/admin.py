from django.contrib import admin
from .models import AuditLog, School

# Register your models here.
admin.site.register(AuditLog)
admin.site.register(School)

admin.site.site_header = 'Grant Tracker Administration'
admin.site.site_title = 'Grant Tracker Admin'
admin.site.index_title = 'Welcome to Grant Tracker Administration'
