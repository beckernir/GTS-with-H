from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from core.models import User, School
import uuid


class TrainingCategory(models.Model):
    """
    Model for organizing training courses into categories.
    """
    
    # Category types
    CATEGORY_TYPE_CHOICES = [
        ('grant_management', 'Grant Management'),
        ('financial_management', 'Financial Management'),
        ('project_management', 'Project Management'),
        ('compliance', 'Compliance and Regulations'),
        ('technology', 'Technology and ICT'),
        ('leadership', 'Leadership and Management'),
        ('pedagogy', 'Teaching and Pedagogy'),
        ('special_needs', 'Special Needs Education'),
        ('other', 'Other'),
    ]
    
    # Core fields
    category_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    category_name = models.CharField(max_length=100, unique=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPE_CHOICES, default='other')
    description = models.TextField()
    
    # Category settings
    is_active = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=False)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_training_categories')
    
    class Meta:
        db_table = 'training_training_category'
        verbose_name = 'Training Category'
        verbose_name_plural = 'Training Categories'
        ordering = ['category_type', 'category_name']
    
    def __str__(self):
        return f"{self.category_name} ({self.get_category_type_display()})"


class TrainingCourse(models.Model):
    """
    Model for training courses and programs.
    """
    
    # Course levels
    COURSE_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    # Course formats
    COURSE_FORMAT_CHOICES = [
        ('online', 'Online'),
        ('in_person', 'In-Person'),
        ('hybrid', 'Hybrid'),
        ('self_paced', 'Self-Paced'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
    ]
    
    # Core fields
    course_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    course_title = models.CharField(max_length=200, unique=True)
    course_code = models.CharField(max_length=20, unique=True, help_text="Auto-generated course code")
    
    # Course details
    category = models.ForeignKey(TrainingCategory, on_delete=models.CASCADE, related_name='courses')
    description = models.TextField()
    learning_objectives = models.TextField()
    target_audience = models.TextField()
    
    # Course specifications
    course_level = models.CharField(max_length=20, choices=COURSE_LEVEL_CHOICES, default='beginner')
    course_format = models.CharField(max_length=20, choices=COURSE_FORMAT_CHOICES, default='online')
    duration_hours = models.PositiveIntegerField(default=0)
    max_participants = models.PositiveIntegerField(default=0, help_text="0 for unlimited")
    
    # Course content
    course_materials = models.TextField(blank=True, null=True)
    prerequisites = models.TextField(blank=True, null=True)
    certification_requirements = models.TextField(blank=True, null=True)
    # Guide fields for help/training
    video_url = models.URLField(blank=True, null=True, help_text="YouTube or Vimeo link for training video")
    guide_document = models.FileField(upload_to='training_guides/', blank=True, null=True, help_text="Upload a PDF or DOCX guide")
    
    # Course status
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    approval_date = models.DateTimeField(blank=True, null=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_training_courses')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_training_courses')
    
    class Meta:
        db_table = 'training_training_course'
        verbose_name = 'Training Course'
        verbose_name_plural = 'Training Courses'
        ordering = ['category', 'course_title']
    
    def __str__(self):
        return f"{self.course_title} ({self.course_code})"
    
    def save(self, *args, **kwargs):
        if not self.course_code:
            super().save(*args, **kwargs)  # Save to get an ID
            self.course_code = f"TC{timezone.now().strftime('%Y%m')}{self.pk:04d}"
            super().save(update_fields=['course_code'])
        else:
            super().save(*args, **kwargs)


class CourseModule(models.Model):
    """
    Model for individual modules within a training course.
    """
    
    # Module types
    MODULE_TYPE_CHOICES = [
        ('video', 'Video Lecture'),
        ('document', 'Document/Reading'),
        ('quiz', 'Quiz/Assessment'),
        ('assignment', 'Assignment'),
        ('discussion', 'Discussion Forum'),
        ('practical', 'Practical Exercise'),
        ('other', 'Other'),
    ]
    
    # Core fields
    module_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    course = models.ForeignKey(TrainingCourse, on_delete=models.CASCADE, related_name='modules')
    module_title = models.CharField(max_length=200)
    module_type = models.CharField(max_length=20, choices=MODULE_TYPE_CHOICES, default='video')
    
    # Module details
    description = models.TextField()
    content = models.TextField(blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(default=0)
    
    # Module order
    order = models.PositiveIntegerField(default=0, help_text="Order within the course")
    
    # Module requirements
    is_required = models.BooleanField(default=True)
    passing_score = models.PositiveIntegerField(default=70, help_text="Minimum score to pass (0-100)")
    
    # Module files
    module_file = models.FileField(upload_to='course_modules/', blank=True, null=True)
    supplementary_files = models.JSONField(default=list, help_text="JSON array of supplementary file paths")
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_course_modules')
    
    class Meta:
        db_table = 'training_course_module'
        verbose_name = 'Course Module'
        verbose_name_plural = 'Course Modules'
        ordering = ['course', 'order']
        unique_together = ['course', 'order']
    
    def __str__(self):
        return f"{self.module_title} - {self.course.course_title}"


class TrainingSession(models.Model):
    """
    Model for scheduled training sessions.
    """
    
    # Session status choices
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('postponed', 'Postponed'),
    ]
    
    # Core fields
    session_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    course = models.ForeignKey(TrainingCourse, on_delete=models.CASCADE, related_name='sessions')
    session_title = models.CharField(max_length=200)
    
    # Session details
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True, null=True)
    
    # Session capacity
    max_participants = models.PositiveIntegerField(default=0)
    current_participants = models.PositiveIntegerField(default=0)
    
    # Session status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    # Session facilitators
    facilitators = models.ManyToManyField(User, related_name='facilitated_sessions', blank=True)
    
    # Session notes
    session_notes = models.TextField(blank=True, null=True)
    completion_notes = models.TextField(blank=True, null=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_training_sessions')
    
    class Meta:
        db_table = 'training_training_session'
        verbose_name = 'Training Session'
        verbose_name_plural = 'Training Sessions'
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.session_title} - {self.course.course_title}"
    
    def get_duration_hours(self):
        """Calculate session duration in hours."""
        duration = self.end_date - self.start_date
        return duration.total_seconds() / 3600
    
    def is_full(self):
        """Check if session is at full capacity."""
        if self.max_participants == 0:
            return False
        return self.current_participants >= self.max_participants
    
    def get_available_slots(self):
        """Get number of available slots."""
        if self.max_participants == 0:
            return float('inf')
        return max(0, self.max_participants - self.current_participants)


class TrainingEnrollment(models.Model):
    """
    Model for tracking user enrollments in training courses.
    """
    
    # Enrollment status choices
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('failed', 'Failed'),
    ]
    
    # Core fields
    enrollment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_enrollments')
    course = models.ForeignKey(TrainingCourse, on_delete=models.CASCADE, related_name='enrollments')
    session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE, related_name='enrollments', null=True, blank=True)
    
    # Enrollment details
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    
    # Progress tracking
    start_date = models.DateTimeField(blank=True, null=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Assessment results
    final_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_certified = models.BooleanField(default=False)
    certification_date = models.DateTimeField(blank=True, null=True)
    
    # Enrollment notes
    enrollment_notes = models.TextField(blank=True, null=True)
    completion_notes = models.TextField(blank=True, null=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'training_training_enrollment'
        verbose_name = 'Training Enrollment'
        verbose_name_plural = 'Training Enrollments'
        ordering = ['-enrollment_date']
        unique_together = ['user', 'course', 'session']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.course.course_title}"
    
    def get_duration_days(self):
        """Calculate enrollment duration in days."""
        if self.start_date and self.completion_date:
            duration = self.completion_date - self.start_date
            return duration.days
        return 0


class ModuleProgress(models.Model):
    """
    Model for tracking individual module progress within a course enrollment.
    """
    
    # Progress status choices
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    # Core fields
    progress_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    enrollment = models.ForeignKey(TrainingEnrollment, on_delete=models.CASCADE, related_name='module_progress')
    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='progress_records')
    
    # Progress details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    start_date = models.DateTimeField(blank=True, null=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    
    # Assessment results
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    attempts = models.PositiveIntegerField(default=0)
    time_spent_minutes = models.PositiveIntegerField(default=0)
    
    # Progress notes
    notes = models.TextField(blank=True, null=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'training_module_progress'
        verbose_name = 'Module Progress'
        verbose_name_plural = 'Module Progress'
        ordering = ['enrollment', 'module__order']
        unique_together = ['enrollment', 'module']
    
    def __str__(self):
        return f"{self.enrollment.user.get_full_name()} - {self.module.module_title}"
    
    def is_passed(self):
        """Check if module was passed based on score."""
        return self.score >= self.module.passing_score


class TrainingAssessment(models.Model):
    """
    Model for training assessments and quizzes.
    """
    
    # Assessment types
    ASSESSMENT_TYPE_CHOICES = [
        ('quiz', 'Quiz'),
        ('exam', 'Exam'),
        ('assignment', 'Assignment'),
        ('practical', 'Practical Assessment'),
        ('survey', 'Survey'),
        ('other', 'Other'),
    ]
    
    # Core fields
    assessment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='assessments')
    assessment_title = models.CharField(max_length=200)
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPE_CHOICES, default='quiz')
    
    # Assessment details
    description = models.TextField()
    instructions = models.TextField(blank=True, null=True)
    time_limit_minutes = models.PositiveIntegerField(default=0, help_text="0 for no time limit")
    
    # Assessment settings
    passing_score = models.PositiveIntegerField(default=70)
    max_attempts = models.PositiveIntegerField(default=1)
    is_required = models.BooleanField(default=True)
    
    # Assessment content
    questions = models.JSONField(default=list, help_text="JSON array containing assessment questions")
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_assessments')
    
    class Meta:
        db_table = 'training_training_assessment'
        verbose_name = 'Training Assessment'
        verbose_name_plural = 'Training Assessments'
        ordering = ['module', 'assessment_title']
    
    def __str__(self):
        return f"{self.assessment_title} - {self.module.module_title}"


class AssessmentResult(models.Model):
    """
    Model for storing assessment results and responses.
    """
    
    # Result status choices
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ]
    
    # Core fields
    result_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    enrollment = models.ForeignKey(TrainingEnrollment, on_delete=models.CASCADE, related_name='assessment_results')
    assessment = models.ForeignKey(TrainingAssessment, on_delete=models.CASCADE, related_name='results')
    
    # Result details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    
    # Assessment results
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    total_questions = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    
    # Response data
    responses = models.JSONField(default=dict, help_text="JSON object containing user responses")
    time_spent_minutes = models.PositiveIntegerField(default=0)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'training_assessment_result'
        verbose_name = 'Assessment Result'
        verbose_name_plural = 'Assessment Results'
        ordering = ['-start_time']
    
    def __str__(self):
        return f"{self.enrollment.user.get_full_name()} - {self.assessment.assessment_title}"
    
    def is_passed(self):
        """Check if assessment was passed."""
        return self.score >= self.assessment.passing_score
    
    def get_accuracy_percentage(self):
        """Calculate accuracy percentage."""
        if self.total_questions > 0:
            return (self.correct_answers / self.total_questions) * 100
        return 0


class TrainingCertificate(models.Model):
    """
    Model for training certificates and achievements.
    """
    
    # Certificate types
    CERTIFICATE_TYPE_CHOICES = [
        ('completion', 'Course Completion'),
        ('achievement', 'Achievement'),
        ('participation', 'Participation'),
        ('excellence', 'Excellence'),
        ('specialization', 'Specialization'),
    ]
    
    # Core fields
    certificate_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    enrollment = models.ForeignKey(TrainingEnrollment, on_delete=models.CASCADE, related_name='certificates')
    certificate_type = models.CharField(max_length=20, choices=CERTIFICATE_TYPE_CHOICES, default='completion')
    
    # Certificate details
    certificate_title = models.CharField(max_length=200)
    certificate_number = models.CharField(max_length=50, unique=True, help_text="Auto-generated certificate number")
    issue_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    
    # Certificate content
    description = models.TextField()
    achievements = models.JSONField(default=list, help_text="JSON array of achievements")
    
    # Certificate file
    certificate_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    
    # Certificate status
    is_valid = models.BooleanField(default=True)
    is_revoked = models.BooleanField(default=False)
    revocation_reason = models.TextField(blank=True, null=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='issued_certificates')
    
    class Meta:
        db_table = 'training_training_certificate'
        verbose_name = 'Training Certificate'
        verbose_name_plural = 'Training Certificates'
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"{self.certificate_title} - {self.enrollment.user.get_full_name()}"
    
    def save(self, *args, **kwargs):
        # Auto-generate certificate number if not set
        if not self.certificate_number:
            super().save(*args, **kwargs)  # Save to get an ID
            self.certificate_number = f"CERT{timezone.now().strftime('%Y%m')}{self.id:06d}"
            super().save(update_fields=['certificate_number'])
        else:
            super().save(*args, **kwargs)
    
    def is_expired(self):
        """Check if certificate has expired."""
        if self.expiry_date:
            return timezone.now() > self.expiry_date
        return False
