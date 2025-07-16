from django import forms
from .models import School
from .models import User
from reporting.models import SupplierCriterion

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = [
            'school_name', 'school_code', 'district', 'sector', 'cell', 'village',
            'level', 'total_students', 'total_teachers', 'total_staff',
            'phone_number', 'email_address', 'website', 'address',
            'latitude', 'longitude', 'status', 'principal_name', 'principal_phone', 'principal_email',
            'academic_performance_score', 'infrastructure_score', 'need_score'
        ]
        widgets = {
            'school_name': forms.TextInput(attrs={'class': 'form-control'}),
            'school_code': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'sector': forms.TextInput(attrs={'class': 'form-control'}),
            'cell': forms.TextInput(attrs={'class': 'form-control'}),
            'village': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-select'}),
            'total_students': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_teachers': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_staff': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'principal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'principal_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'principal_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'academic_performance_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'infrastructure_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'need_score': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'role', 'status',
            'phone_number', 'profile_picture', 'date_of_birth', 'address', 'emergency_contact'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user 

class SupplierRegistrationWithCriteriaForm(UserCreateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically add fields for all active supplier criteria
        for criterion in SupplierCriterion.objects.filter(active=True).order_by('ordering', 'name'):
            field_name = f'criterion_{criterion.id}'
            if criterion.type == 'file':
                self.fields[field_name] = forms.FileField(
                    label=criterion.name,
                    required=criterion.required,
                    help_text=criterion.description,
                )
            elif criterion.type == 'text':
                self.fields[field_name] = forms.CharField(
                    label=criterion.name,
                    required=criterion.required,
                    help_text=criterion.description,
                    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
                )
            elif criterion.type == 'boolean':
                self.fields[field_name] = forms.BooleanField(
                    label=criterion.name,
                    required=criterion.required,
                    help_text=criterion.description,
                )
            self.fields[field_name].criterion_obj = criterion 