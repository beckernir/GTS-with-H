from django import forms
from .models import CommunityForum, ForumTopic, ForumPost, Announcement, CommunityEvent, CommunityMessage
from core.models import User


class CommunityForumForm(forms.ModelForm):
    class Meta:
        model = CommunityForum
        fields = [
            'forum_name', 'forum_type', 'access_level', 'description', 'rules',
            'school', 'is_active', 'requires_moderation', 'allow_anonymous', 'moderators'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'rules': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = 'form-control'
            if isinstance(field.widget, forms.CheckboxInput):
                css_class = ''  # Avoid overriding checkbox styling
            field.widget.attrs.setdefault('class', css_class)


class ForumTopicForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Enter tags separated by commas (e.g. tag1, tag2, tag3)",
        widget=forms.TextInput(attrs={'placeholder': 'tag1, tag2, tag3'})
    )

    class Meta:
        model = ForumTopic
        fields = ['forum', 'topic_title', 'content', 'status', 'is_sticky', 'is_announcement', 'allow_replies', 'tags']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show tags as comma-separated string
        if self.instance and self.instance.pk:
            self.fields['tags'].initial = ', '.join(self.instance.tags or [])
        for field in self.fields.values():
            css_class = 'form-control'
            if isinstance(field.widget, forms.CheckboxInput):
                css_class = ''
            field.widget.attrs.setdefault('class', css_class)

    def clean_tags(self):
        data = self.cleaned_data['tags']
        if data:
            return [tag.strip() for tag in data.split(',') if tag.strip()]
        return []


class ForumPostForm(forms.ModelForm):
    attachments = forms.CharField(
        required=False,
        help_text="Enter attachment file paths separated by commas",
        widget=forms.TextInput(attrs={'placeholder': 'file1.pdf, file2.jpg'})
    )

    class Meta:
        model = ForumPost
        fields = ['topic', 'parent_post', 'content', 'status', 'attachments']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['attachments'].initial = ', '.join(self.instance.attachments or [])
        for field in self.fields.values():
            css_class = 'form-control'
            if isinstance(field.widget, forms.CheckboxInput):
                css_class = ''
            field.widget.attrs.setdefault('class', css_class)

    def clean_attachments(self):
        data = self.cleaned_data['attachments']
        if data:
            return [att.strip() for att in data.split(',') if att.strip()]
        return []


class AnnouncementForm(forms.ModelForm):
    target_audience = forms.CharField(
        required=False,
        help_text="Enter target user roles separated by commas",
        widget=forms.TextInput(attrs={'placeholder': 'role1, role2'})
    )
    attachments = forms.CharField(
        required=False,
        help_text="Enter attachment file paths separated by commas",
        widget=forms.TextInput(attrs={'placeholder': 'file1.pdf, file2.jpg'})
    )

    class Meta:
        model = Announcement
        fields = [
            'announcement_type', 'priority', 'title', 'content', 'summary', 'target_audience', 'target_schools',
            'publish_date', 'expiry_date', 'is_active', 'requires_acknowledgment',
            'show_on_dashboard', 'send_email_notification', 'attachments'
        ]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
            'summary': forms.Textarea(attrs={'rows': 2}),
            'publish_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['target_audience'].initial = ', '.join(self.instance.target_audience or [])
            self.fields['attachments'].initial = ', '.join(self.instance.attachments or [])
        for field in self.fields.values():
            css_class = 'form-control'
            if isinstance(field.widget, forms.CheckboxInput):
                css_class = ''
            field.widget.attrs.setdefault('class', css_class)

    def clean_target_audience(self):
        data = self.cleaned_data['target_audience']
        if data:
            return [aud.strip() for aud in data.split(',') if aud.strip()]
        return []

    def clean_attachments(self):
        data = self.cleaned_data['attachments']
        if data:
            return [att.strip() for att in data.split(',') if att.strip()]
        return []


class CommunityEventForm(forms.ModelForm):
    target_audience = forms.CharField(
        required=False,
        help_text="Enter target user roles separated by commas",
        widget=forms.TextInput(attrs={'placeholder': 'role1, role2'})
    )
    event_materials = forms.CharField(
        required=False,
        help_text="Enter event material file paths separated by commas",
        widget=forms.TextInput(attrs={'placeholder': 'file1.pdf, file2.jpg'})
    )

    class Meta:
        model = CommunityEvent
        fields = [
            'event_type', 'status', 'event_title', 'description', 'objectives', 'start_date', 'end_date',
            'registration_deadline', 'location', 'is_virtual', 'virtual_meeting_link', 'max_participants',
            'organizers', 'contact_person', 'target_audience', 'target_schools', 'event_materials'
        ] 
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'objectives': forms.Textarea(attrs={'rows': 2}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'registration_deadline': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['target_audience'].initial = ', '.join(self.instance.target_audience or [])
            self.fields['event_materials'].initial = ', '.join(self.instance.event_materials or [])
        for field in self.fields.values():
            css_class = 'form-control'
            if isinstance(field.widget, forms.CheckboxInput):
                css_class = ''
            field.widget.attrs.setdefault('class', css_class)

    def clean_target_audience(self):
        data = self.cleaned_data['target_audience']
        if data:
            return [aud.strip() for aud in data.split(',') if aud.strip()]
        return []

    def clean_event_materials(self):
        data = self.cleaned_data['event_materials']
        if data:
            return [mat.strip() for mat in data.split(',') if mat.strip()]
        return []


class CommunityMessageForm(forms.ModelForm):
    recipients = forms.CharField(
        help_text="Enter recipient usernames separated by commas or use @mention.",
        widget=forms.TextInput(attrs={'placeholder': '@username1, @username2'})
    )
    class Meta:
        model = CommunityMessage
        fields = ['recipients', 'subject', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }
    def clean_recipients(self):
        data = self.cleaned_data['recipients']
        usernames = [u.strip().lstrip('@') for u in data.split(',') if u.strip()]
        users = list(User.objects.filter(username__in=usernames))
        if not users:
            raise forms.ValidationError('No valid recipients found.')
        return users
