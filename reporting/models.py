from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from core.models import User, School
from grants.models import GrantProposal, GrantCategory
from budget.models import SchoolBudget, BudgetPeriod
import uuid


class Dashboard(models.Model):
    """
    Model for user dashboards and personalized views.
    """
    
    # Dashboard types
    DASHBOARD_TYPE_CHOICES = [
        ('reb_officer', 'REB Officer Dashboard'),
        ('school_admin', 'School Administrator Dashboard'),
        ('teacher', 'Teacher Dashboard'),
        ('community', 'Community Dashboard'),
        ('system_admin', 'System Administrator Dashboard'),
        ('custom', 'Custom Dashboard'),
    ]
    
    # Core fields
    dashboard_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    dashboard_name = models.CharField(max_length=200)
    dashboard_type = models.CharField(max_length=20, choices=DASHBOARD_TYPE_CHOICES, default='custom')
    
    # Dashboard details
    description = models.TextField(blank=True, null=True)
    layout_config = models.JSONField(default=dict, help_text="JSON object containing dashboard layout configuration")
    
    # Dashboard scope
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboards')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='dashboards', null=True, blank=True)
    
    # Dashboard settings
    is_default = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    refresh_interval = models.PositiveIntegerField(default=300, help_text="Refresh interval in seconds")
    
    # Dashboard status
    is_active = models.BooleanField(default=True)
    last_accessed = models.DateTimeField(blank=True, null=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reporting_dashboard'
        verbose_name = 'Dashboard'
        verbose_name_plural = 'Dashboards'
        ordering = ['-is_default', '-created_at']
        unique_together = ['user', 'dashboard_name']
    
    def __str__(self):
        return f"{self.dashboard_name} - {self.user.get_full_name()}"


class DashboardWidget(models.Model):
    """
    Model for dashboard widgets and components.
    """
    
    # Widget types
    WIDGET_TYPE_CHOICES = [
        ('chart', 'Chart/Graph'),
        ('table', 'Data Table'),
        ('metric', 'KPI Metric'),
        ('list', 'List View'),
        ('calendar', 'Calendar'),
        ('map', 'Map View'),
        ('gauge', 'Gauge Chart'),
        ('progress', 'Progress Bar'),
        ('summary', 'Summary Card'),
        ('custom', 'Custom Widget'),
    ]
    
    # Chart types
    CHART_TYPE_CHOICES = [
        ('line', 'Line Chart'),
        ('bar', 'Bar Chart'),
        ('pie', 'Pie Chart'),
        ('doughnut', 'Doughnut Chart'),
        ('area', 'Area Chart'),
        ('scatter', 'Scatter Plot'),
        ('heatmap', 'Heatmap'),
        ('treemap', 'Treemap'),
        ('other', 'Other'),
    ]
    
    # Core fields
    widget_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='widgets')
    widget_name = models.CharField(max_length=200)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPE_CHOICES, default='metric')
    
    # Widget configuration
    chart_type = models.CharField(max_length=20, choices=CHART_TYPE_CHOICES, blank=True, null=True)
    data_source = models.CharField(max_length=100, help_text="Data source identifier")
    configuration = models.JSONField(default=dict, help_text="JSON object containing widget configuration")
    
    # Widget layout
    position_x = models.PositiveIntegerField(default=0)
    position_y = models.PositiveIntegerField(default=0)
    width = models.PositiveIntegerField(default=1)
    height = models.PositiveIntegerField(default=1)
    
    # Widget settings
    is_visible = models.BooleanField(default=True)
    auto_refresh = models.BooleanField(default=True)
    refresh_interval = models.PositiveIntegerField(default=300, help_text="Refresh interval in seconds")
    
    # Widget data
    last_data_update = models.DateTimeField(blank=True, null=True)
    cached_data = models.JSONField(default=dict, help_text="JSON object containing cached widget data")
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reporting_dashboard_widget'
        verbose_name = 'Dashboard Widget'
        verbose_name_plural = 'Dashboard Widgets'
        ordering = ['dashboard', 'position_y', 'position_x']
    
    def __str__(self):
        return f"{self.widget_name} - {self.dashboard.dashboard_name}"


class KPI(models.Model):
    """
    Model for Key Performance Indicators and metrics.
    """
    
    # KPI categories
    KPI_CATEGORY_CHOICES = [
        ('financial', 'Financial KPIs'),
        ('operational', 'Operational KPIs'),
        ('academic', 'Academic KPIs'),
        ('compliance', 'Compliance KPIs'),
        ('user_engagement', 'User Engagement KPIs'),
        ('system_performance', 'System Performance KPIs'),
        ('other', 'Other KPIs'),
    ]
    
    # KPI types
    KPI_TYPE_CHOICES = [
        ('count', 'Count'),
        ('percentage', 'Percentage'),
        ('currency', 'Currency'),
        ('ratio', 'Ratio'),
        ('score', 'Score'),
        ('duration', 'Duration'),
        ('other', 'Other'),
    ]
    
    # Core fields
    kpi_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    kpi_name = models.CharField(max_length=200, unique=True)
    kpi_category = models.CharField(max_length=20, choices=KPI_CATEGORY_CHOICES, default='other')
    kpi_type = models.CharField(max_length=20, choices=KPI_TYPE_CHOICES, default='count')
    
    # KPI details
    description = models.TextField()
    calculation_formula = models.TextField(help_text="Formula or method for calculating the KPI")
    unit_of_measure = models.CharField(max_length=50, blank=True, null=True)
    
    # KPI targets
    target_value = models.DecimalField(max_digits=15, decimal_places=4, default=0.0000)
    threshold_value = models.DecimalField(max_digits=15, decimal_places=4, default=0.0000)
    min_value = models.DecimalField(max_digits=15, decimal_places=4, default=0.0000)
    max_value = models.DecimalField(max_digits=15, decimal_places=4, default=100.0000)
    
    # KPI settings
    is_active = models.BooleanField(default=True)
    is_system = models.BooleanField(default=False, help_text="System KPIs cannot be modified by users")
    auto_calculate = models.BooleanField(default=True)
    
    # KPI scope
    applicable_roles = models.JSONField(default=list, help_text="JSON array of user roles this KPI applies to")
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_kpis')
    
    class Meta:
        db_table = 'reporting_kpi'
        verbose_name = 'KPI'
        verbose_name_plural = 'KPIs'
        ordering = ['kpi_category', 'kpi_name']
    
    def __str__(self):
        return f"{self.kpi_name} ({self.get_kpi_category_display()})"


class KPIValue(models.Model):
    """
    Model for storing KPI values over time.
    """
    
    # Core fields
    value_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE, related_name='values')
    
    # Value details
    value = models.DecimalField(max_digits=15, decimal_places=4)
    measurement_date = models.DateField()
    measurement_period = models.CharField(max_length=50, help_text="e.g., '2024 Q1', 'Monthly', 'Weekly'")
    
    # Value context
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='kpi_values', null=True, blank=True)
    context_data = models.JSONField(default=dict, help_text="JSON object containing additional context data")
    
    # Performance tracking
    is_above_target = models.BooleanField(default=False)
    is_above_threshold = models.BooleanField(default=False)
    performance_status = models.CharField(max_length=20, choices=[
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('critical', 'Critical'),
    ], default='fair')
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    calculated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='calculated_kpi_values')
    
    class Meta:
        db_table = 'reporting_kpi_value'
        verbose_name = 'KPI Value'
        verbose_name_plural = 'KPI Values'
        ordering = ['kpi', '-measurement_date']
        unique_together = ['kpi', 'school', 'measurement_date']
    
    def __str__(self):
        return f"{self.kpi.kpi_name}: {self.value} ({self.measurement_date})"


class Report(models.Model):
    """
    Model for system reports and analytics.
    """
    
    # Report types
    REPORT_TYPE_CHOICES = [
        ('grant_summary', 'Grant Summary Report'),
        ('budget_analysis', 'Budget Analysis Report'),
        ('school_performance', 'School Performance Report'),
        ('compliance_report', 'Compliance Report'),
        ('training_report', 'Training Report'),
        ('user_activity', 'User Activity Report'),
        ('financial_report', 'Financial Report'),
        ('custom', 'Custom Report'),
    ]
    
    # Report formats
    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
        ('json', 'JSON'),
        ('html', 'HTML'),
        ('other', 'Other'),
    ]
    
    # Core fields
    report_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    report_name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES, default='custom')
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='pdf')
    
    # Report details
    description = models.TextField(blank=True, null=True)
    parameters = models.JSONField(default=dict, help_text="JSON object containing report parameters")
    
    # Report scope
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_reports')
    
    # Report scheduling
    is_scheduled = models.BooleanField(default=False)
    schedule_frequency = models.CharField(max_length=20, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
        ('custom', 'Custom'),
    ], blank=True, null=True)
    next_run_date = models.DateTimeField(blank=True, null=True)
    
    # Report file
    report_file = models.FileField(upload_to='reports/', blank=True, null=True)
    file_size = models.PositiveIntegerField(default=0, help_text="File size in bytes")
    
    # Report status
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('generating', 'Generating'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    
    # Report metadata
    generation_time_seconds = models.PositiveIntegerField(default=0)
    row_count = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True, null=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    generated_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'reporting_report'
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.report_name} ({self.get_report_type_display()})"


class AnalyticsEvent(models.Model):
    """
    Model for tracking analytics events and user interactions.
    """
    
    # Event types
    EVENT_TYPE_CHOICES = [
        ('page_view', 'Page View'),
        ('button_click', 'Button Click'),
        ('form_submit', 'Form Submit'),
        ('file_download', 'File Download'),
        ('report_generate', 'Report Generation'),
        ('data_export', 'Data Export'),
        ('search', 'Search'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('other', 'Other'),
    ]
    
    # Core fields
    event_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='other')
    event_name = models.CharField(max_length=200)
    
    # Event details
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analytics_events')
    session_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Event context
    page_url = models.URLField(blank=True, null=True)
    referrer_url = models.URLField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    
    # Event data
    event_data = models.JSONField(default=dict, help_text="JSON object containing event-specific data")
    metadata = models.JSONField(default=dict, help_text="JSON object containing additional metadata")
    
    # Event timing
    timestamp = models.DateTimeField(auto_now_add=True)
    duration_seconds = models.PositiveIntegerField(default=0, help_text="Event duration in seconds")
    
    class Meta:
        db_table = 'reporting_analytics_event'
        verbose_name = 'Analytics Event'
        verbose_name_plural = 'Analytics Events'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.event_name} - {self.user.get_full_name()} ({self.timestamp})"


class DataExport(models.Model):
    """
    Model for tracking data exports and downloads.
    """
    
    # Export types
    EXPORT_TYPE_CHOICES = [
        ('grants', 'Grants Data'),
        ('budgets', 'Budget Data'),
        ('reports', 'Reports Data'),
        ('users', 'Users Data'),
        ('schools', 'Schools Data'),
        ('training', 'Training Data'),
        ('analytics', 'Analytics Data'),
        ('custom', 'Custom Export'),
    ]
    
    # Export formats
    FORMAT_CHOICES = [
        ('csv', 'CSV'),
        ('excel', 'Excel'),
        ('json', 'JSON'),
        ('xml', 'XML'),
        ('pdf', 'PDF'),
        ('other', 'Other'),
    ]
    
    # Core fields
    export_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    export_type = models.CharField(max_length=20, choices=EXPORT_TYPE_CHOICES, default='custom')
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='csv')
    
    # Export details
    description = models.TextField(blank=True, null=True)
    filters = models.JSONField(default=dict, help_text="JSON object containing export filters")
    
    # Export scope
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='data_exports')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='data_exports', null=True, blank=True)
    
    # Export file
    export_file = models.FileField(upload_to='exports/', blank=True, null=True)
    file_size = models.PositiveIntegerField(default=0, help_text="File size in bytes")
    
    # Export status
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    
    # Export metadata
    row_count = models.PositiveIntegerField(default=0)
    processing_time_seconds = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True, null=True)
    
    # Export tracking
    download_count = models.PositiveIntegerField(default=0)
    last_downloaded = models.DateTimeField(blank=True, null=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'reporting_data_export'
        verbose_name = 'Data Export'
        verbose_name_plural = 'Data Exports'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_export_type_display()} Export - {self.user.get_full_name()}"


class ReportSchedule(models.Model):
    """
    Model for scheduled report generation.
    """
    
    # Schedule frequencies
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
        ('custom', 'Custom'),
    ]
    
    # Core fields
    schedule_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    schedule_name = models.CharField(max_length=200)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='schedules')
    
    # Schedule details
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='monthly')
    frequency_config = models.JSONField(default=dict, help_text="JSON object containing frequency configuration")
    
    # Schedule timing
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    next_run = models.DateTimeField()
    
    # Schedule settings
    is_active = models.BooleanField(default=True)
    send_email = models.BooleanField(default=False)
    email_recipients = models.JSONField(default=list, help_text="JSON array of email addresses")
    
    # Schedule tracking
    last_run = models.DateTimeField(blank=True, null=True)
    total_runs = models.PositiveIntegerField(default=0)
    successful_runs = models.PositiveIntegerField(default=0)
    failed_runs = models.PositiveIntegerField(default=0)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_schedules')
    
    class Meta:
        db_table = 'reporting_report_schedule'
        verbose_name = 'Report Schedule'
        verbose_name_plural = 'Report Schedules'
        ordering = ['-next_run']
    
    def __str__(self):
        return f"{self.schedule_name} - {self.report.report_name}"
    
    def get_success_rate(self):
        """Calculate success rate percentage."""
        if self.total_runs > 0:
            return (self.successful_runs / self.total_runs) * 100
        return 0
