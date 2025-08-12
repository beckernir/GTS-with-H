from django import forms
from .models import NotificationPreference, Notification


class NotificationPreferenceForm(forms.ModelForm):
    """Form for user notification preferences."""
    
    class Meta:
        model = NotificationPreference
        fields = [
            'email_notifications',
            'sms_notifications', 
            'in_app_notifications',
            'email_frequency',
            'sms_frequency',
            'grant_notifications',
            'budget_notifications',
            'training_notifications',
            'system_notifications',
            'quiet_hours_enabled',
            'quiet_hours_start',
            'quiet_hours_end',
        ]
        widgets = {
            'quiet_hours_start': forms.TimeInput(attrs={'type': 'time'}),
            'quiet_hours_end': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        quiet_hours_enabled = cleaned_data.get('quiet_hours_enabled')
        quiet_hours_start = cleaned_data.get('quiet_hours_start')
        quiet_hours_end = cleaned_data.get('quiet_hours_end')
        
        if quiet_hours_enabled:
            if not quiet_hours_start or not quiet_hours_end:
                raise forms.ValidationError(
                    "Start and end times are required when quiet hours are enabled."
                )
            
            if quiet_hours_start >= quiet_hours_end:
                raise forms.ValidationError(
                    "End time must be after start time."
                )
        
        return cleaned_data


class NotificationCreateForm(forms.ModelForm):
    """Form for creating new notifications (admin only)."""
    
    target_roles = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select user roles to receive this notification"
    )
    
    target_schools = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select schools to receive this notification"
    )
    
    scheduled_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        help_text="Schedule notification for later (optional)"
    )
    
    expires_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        help_text="Set expiration date (optional)"
    )
    
    class Meta:
        model = Notification
        fields = [
            'title',
            'message',
            'summary',
            'notification_type',
            'priority',
            'requires_action',
            'action_url',
            'action_text',
            'send_email',
            'send_sms',
            'scheduled_at',
            'expires_at',
            'is_active',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'action_url': forms.URLInput(attrs={'class': 'form-control'}),
            'action_text': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set choices for target roles and schools
        from core.models import User, School
        
        self.fields['target_roles'].choices = User.ROLE_CHOICES
        self.fields['target_schools'].choices = [(school.id, school.school_name) for school in School.objects.all()]
        
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            if hasattr(field, 'widget') and hasattr(field.widget, 'attrs'):
                field.widget.attrs.update({'class': 'form-control'})
    
    def clean(self):
        cleaned_data = super().clean()
        scheduled_at = cleaned_data.get('scheduled_at')
        expires_at = cleaned_data.get('expires_at')
        
        if scheduled_at and expires_at and scheduled_at >= expires_at:
            raise forms.ValidationError(
                "Expiration date must be after scheduled date."
            )
        
        return cleaned_data


class NotificationFilterForm(forms.Form):
    """Form for filtering notifications."""
    
    STATUS_CHOICES = [
        ('all', 'All'),
        ('unread', 'Unread'),
        ('read', 'Read'),
        ('archived', 'Archived'),
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    notification_type = forms.ChoiceField(
        choices=[('all', 'All Types')] + Notification.NOTIFICATION_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    priority = forms.ChoiceField(
        choices=[('all', 'All Priorities')] + Notification.PRIORITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    ) 