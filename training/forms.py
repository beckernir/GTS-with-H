from django import forms
from .models import TrainingCourse, TrainingEnrollment, TrainingCertificate
from django.contrib.auth import get_user_model

class TrainingCourseForm(forms.ModelForm):
    class Meta:
        model = TrainingCourse
        fields = [
            'course_title', 'category', 'description', 'learning_objectives',
            'target_audience', 'course_level', 'course_format', 'duration_hours',
            'max_participants', 'course_materials', 'prerequisites', 'certification_requirements',
            'video_url', 'guide_document', 'is_active'
        ]
        widgets = {
            'course_title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'learning_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'target_audience': forms.TextInput(attrs={'class': 'form-control'}),
            'course_level': forms.Select(attrs={'class': 'form-select'}),
            'course_format': forms.Select(attrs={'class': 'form-select'}),
            'duration_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control'}),
            'course_materials': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'prerequisites': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'certification_requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
            'guide_document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class TrainingEnrollmentForm(forms.ModelForm):
    class Meta:
        model = TrainingEnrollment
        fields = ['user', 'course', 'session', 'status']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('request_user', None)
        super().__init__(*args, **kwargs)
        if not (user and (user.is_staff or (hasattr(user, 'is_school_admin') and user.is_school_admin()))):
            self.fields['user'].widget = forms.HiddenInput()

class TrainingCertificateForm(forms.ModelForm):
    class Meta:
        model = TrainingCertificate
        fields = [
            'enrollment', 'certificate_type', 'certificate_title', 'expiry_date',
            'description', 'achievements', 'certificate_file', 'is_valid'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'form-control form-control-sm'}),
            'achievements': forms.Textarea(attrs={'rows': 2, 'class': 'form-control form-control-sm'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
            'certificate_title': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'certificate_type': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'certificate_file': forms.ClearableFileInput(attrs={'class': 'form-control form-control-sm'}),
        } 