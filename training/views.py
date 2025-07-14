from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from .models import TrainingCourse, TrainingCertificate, TrainingEnrollment, TrainingSession, TrainingCategory, CourseModule, TrainingAssessment, AssessmentResult
from .forms import TrainingCourseForm, TrainingCertificateForm, TrainingEnrollmentForm
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
import json

# Create your views here.

def training_overview_view(request):
    """Overview of all training programs and schedules"""
    courses = TrainingCourse.objects.filter(is_active=True)
    sessions = TrainingSession.objects.filter(status='scheduled')
    enrollments = TrainingEnrollment.objects.all()
    return render(request, "training/overview.html", {
        "courses": courses,
        "sessions": sessions,
        "enrollments": enrollments,
    })

@login_required
def training_list_view(request):
    """List all available training programs"""
    courses = TrainingCourse.objects.filter(is_active=True)
    return render(request, "training/training_list.html", {"courses": courses})

@login_required
def training_detail_view(request, training_id):
    """Detailed view of a specific training program"""
    course = get_object_or_404(TrainingCourse, course_id=training_id)
    return render(request, "training/training_detail.html", {"course": course})

@staff_member_required
def training_create_view(request):
    """Create a new training program"""
    return render(request, "training/training_create.html")

@staff_member_required
def training_edit_view(request, training_id):
    """Edit an existing training program"""
    return render(request, "training/training_edit.html")

@staff_member_required
def training_delete_view(request, training_id):
    """Delete a training program"""
    return render(request, "training/training_delete.html")

@login_required
def training_enrollment_view(request, training_id):
    """Enroll in a training program"""
    return render(request, "training/training_enrollment.html")

@login_required
def training_progress_view(request, training_id):
    """View training progress and completion status"""
    return render(request, "training/training_progress.html")

@staff_member_required
def training_calendar_view(request):
    """Calendar view of training schedules"""
    return render(request, "training/training_calendar.html")

@staff_member_required
def training_reports_view(request):
    """Training reports and analytics"""
    return render(request, "training/training_reports.html")

@staff_member_required
def training_materials_view(request, training_id):
    """Manage training materials and resources"""
    return render(request, "training/training_materials.html")

@login_required
def training_certificate_view(request, training_id):
    """View and download training certificates"""
    return render(request, "training/training_certificate.html")

@staff_member_required
def training_feedback_view(request, training_id):
    """View and manage training feedback"""
    return render(request, "training/training_feedback.html")

@staff_member_required
def training_attendance_view(request, training_id):
    """Track training attendance"""
    return render(request, "training/training_attendance.html")

@staff_member_required
def training_evaluation_view(request, training_id):
    """Training evaluation and assessment"""
    return render(request, "training/training_evaluation.html")

@staff_member_required
def training_budget_view(request, training_id):
    """Training budget management"""
    return render(request, "training/training_budget.html")

@staff_member_required
def training_venue_view(request, training_id):
    """Training venue management"""
    return render(request, "training/training_venue.html")

@staff_member_required
def training_instructor_view(request, training_id):
    """Training instructor management"""
    return render(request, "training/training_instructor.html")

@login_required
def training_schedule_view(request, training_id):
    """Training schedule management"""
    return render(request, "training/training_schedule.html")

@staff_member_required
def training_approval_view(request, training_id):
    """Training approval workflow"""
    return render(request, "training/training_approval.html")

@staff_member_required
def training_notification_view(request, training_id):
    """Training notification management"""
    return render(request, "training/training_notification.html")

def category_list_view(request):
    categories = TrainingCategory.objects.filter(is_active=True)
    return render(request, "training/category_list.html", {"categories": categories})

def category_detail_view(request, category_id):
    category = get_object_or_404(TrainingCategory, category_id=category_id)
    return render(request, "training/category_detail.html", {"category": category})

@login_required
def course_list_view(request):
    user = request.user
    if hasattr(user, 'is_reb_officer') and (user.is_reb_officer() or user.is_system_admin()):
        courses = TrainingCourse.objects.all().order_by('-created_at')
    elif hasattr(user, 'is_school_admin') and user.is_school_admin():
        courses = TrainingCourse.objects.filter(created_by=user).order_by('-created_at')
    else:
        courses = TrainingCourse.objects.filter(is_active=True).order_by('-created_at')
    return render(request, "training/course_list.html", {'courses': courses})

@login_required
@user_passes_test(lambda u: hasattr(u, 'is_school_admin') and u.is_school_admin())
def course_create_view(request):
    if request.method == 'POST':
        form = TrainingCourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
            course.save()
            return redirect('training:course_list')
    else:
        form = TrainingCourseForm()
    return render(request, "training/course_create.html", {'form': form})

@login_required
def course_edit_view(request, course_id):
    course = get_object_or_404(TrainingCourse, course_id=course_id)
    user = request.user
    if not (user.is_reb_officer() or user.is_system_admin() or (user.is_school_admin() and course.created_by == user)):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = TrainingCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('training:course_detail', course_id=course.course_id)
    else:
        form = TrainingCourseForm(instance=course)
    return render(request, "training/course_edit.html", {'form': form, 'course': course})

@login_required
def course_detail_view(request, course_id):
    course = get_object_or_404(TrainingCourse, course_id=course_id)
    return render(request, "training/course_detail.html", {'course': course})

def module_list_view(request, course_id):
    modules = CourseModule.objects.filter(course__course_id=course_id).order_by('order')
    return render(request, "training/module_list.html", {"modules": modules})

def module_add_view(request, course_id):
    return render(request, "training/module_add.html")

def module_detail_view(request, module_id):
    module = get_object_or_404(CourseModule, module_id=module_id)
    return render(request, "training/module_detail.html", {"module": module})

def module_edit_view(request, module_id):
    return render(request, "training/module_edit.html")

def module_delete_view(request, module_id):
    return render(request, "training/module_delete.html")

def session_list_view(request):
    sessions = TrainingSession.objects.all().order_by('-start_date')
    total_sessions = sessions.count()
    scheduled = sessions.filter(status='scheduled').count()
    in_progress = sessions.filter(status='in_progress').count()
    completed = sessions.filter(status='completed').count()
    cancelled = sessions.filter(status='cancelled').count()
    can_create = request.user.is_staff or (hasattr(request.user, 'is_school_admin') and request.user.is_school_admin())
    return render(request, "training/session_list.html", {
        'sessions': sessions,
        'total_sessions': total_sessions,
        'scheduled': scheduled,
        'in_progress': in_progress,
        'completed': completed,
        'cancelled': cancelled,
        'can_create': can_create,
    })

def session_create_view(request):
    return render(request, "training/session_create.html")

def session_detail_view(request, session_id):
    session = get_object_or_404(TrainingSession, session_id=session_id)
    return render(request, "training/session_detail.html", {"session": session})

def session_edit_view(request, session_id):
    return render(request, "training/session_edit.html")

def session_register_view(request, session_id):
    return render(request, "training/session_register.html")

@login_required
def enrollment_list_view(request):
    enrollments = TrainingEnrollment.objects.all().select_related('user', 'course')
    total_enrollments = enrollments.count()
    completed = enrollments.filter(status='completed').count()
    in_progress = enrollments.filter(status='in_progress').count()
    dropped = enrollments.filter(status='dropped').count()
    can_create = request.user.is_staff or (hasattr(request.user, 'is_school_admin') and request.user.is_school_admin())
    return render(request, "training/enrollment_list.html", {
        'enrollments': enrollments,
        'total_enrollments': total_enrollments,
        'completed': completed,
        'in_progress': in_progress,
        'dropped': dropped,
        'can_create': can_create,
    })

@login_required
def enrollment_detail_view(request, enrollment_id):
    enrollment = get_object_or_404(TrainingEnrollment, enrollment_id=enrollment_id)
    user = request.user
    if not (user.is_reb_officer() or user.is_system_admin() or enrollment.user == user):
        return HttpResponseForbidden()
    return render(request, "training/enrollment_detail.html", {'enrollment': enrollment})

@login_required
@user_passes_test(lambda u: u.is_staff or (hasattr(u, 'is_school_admin') and u.is_school_admin()))
def enrollment_create_view(request):
    if request.method == 'POST':
        form = TrainingEnrollmentForm(request.POST, request_user=request.user)
        if form.is_valid():
            user = form.cleaned_data['user'] if (request.user.is_staff or (hasattr(request.user, 'is_school_admin') and request.user.is_school_admin())) else request.user
            course = form.cleaned_data['course']
            session = form.cleaned_data.get('session')
            # Prevent duplicate enrollments
            exists = TrainingEnrollment.objects.filter(
                user=user,
                course=course,
                session=session
            ).exists()
            if exists:
                messages.error(request, "This user is already enrolled in this course/session.")
                return redirect('training:enrollment_list')
            enrollment = form.save(commit=False)
            enrollment.user = user
            enrollment.save()
            return redirect('training:enrollment_list')
    else:
        form = TrainingEnrollmentForm(request_user=request.user)
    return render(request, "training/enrollment_create.html", {'form': form})

@login_required
def enrollment_edit_view(request, enrollment_id):
    enrollment = get_object_or_404(TrainingEnrollment, enrollment_id=enrollment_id)
    user = request.user
    if not (user.is_reb_officer() or user.is_system_admin() or (user.is_school_admin() and enrollment.user == user)):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = TrainingEnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            return redirect('training:enrollment_detail', enrollment_id=enrollment.enrollment_id)
    else:
        form = TrainingEnrollmentForm(instance=enrollment)
    return render(request, "training/enrollment_edit.html", {'form': form, 'enrollment': enrollment})

@login_required
def enrollment_delete_view(request, enrollment_id):
    enrollment = get_object_or_404(TrainingEnrollment, enrollment_id=enrollment_id)
    user = request.user
    if not (user.is_reb_officer() or user.is_system_admin() or (user.is_school_admin() and enrollment.user == user)):
        return HttpResponseForbidden()
    if request.method == 'POST':
        enrollment.delete()
        return redirect('training:enrollment_list')
    return render(request, "training/enrollment_delete.html", {'enrollment': enrollment})

def enrollment_progress_view(request, enrollment_id):
    enrollment = get_object_or_404(TrainingEnrollment, enrollment_id=enrollment_id)
    return render(request, "training/enrollment_progress.html", {"enrollment": enrollment})

def module_progress_view(request, module_id):
    module = get_object_or_404(CourseModule, module_id=module_id)
    return render(request, "training/module_progress.html", {"module": module})

def module_progress_update_view(request, module_id):
    return render(request, "training/module_progress_update.html")

def assessment_list_view(request):
    assessments = TrainingAssessment.objects.all().order_by('module__order')
    return render(request, "training/assessment_list.html", {"assessments": assessments})

def assessment_create_view(request):
    return render(request, "training/assessment_create.html")

def assessment_detail_view(request, assessment_id):
    assessment = get_object_or_404(TrainingAssessment, assessment_id=assessment_id)
    return render(request, "training/assessment_detail.html", {"assessment": assessment})

def assessment_take_view(request, assessment_id):
    return render(request, "training/assessment_take.html")

def assessment_submit_view(request, assessment_id):
    return render(request, "training/assessment_submit.html")

def result_list_view(request):
    results = AssessmentResult.objects.all().order_by('-start_time')
    return render(request, "training/result_list.html", {"results": results})

def result_detail_view(request, result_id):
    result = get_object_or_404(AssessmentResult, result_id=result_id)
    return render(request, "training/result_detail.html", {"result": result})

@login_required
@user_passes_test(lambda u: (hasattr(u, 'is_system_admin') and u.is_system_admin()) or (hasattr(u, 'is_school_admin') and u.is_school_admin()) or u.is_staff)
def certificate_create_view(request):
    if request.method == 'POST':
        form = TrainingCertificateForm(request.POST, request.FILES)
        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.created_by = request.user
            certificate.save()
            return redirect('training:certificate_list')
    else:
        form = TrainingCertificateForm()
    return render(request, "training/certificate_create.html", {'form': form})

@login_required
def certificate_list_view(request):
    user = request.user
    if hasattr(user, 'is_reb_officer') and (user.is_reb_officer() or user.is_system_admin()):
        certificates = TrainingCertificate.objects.all().order_by('-issue_date')
    elif hasattr(user, 'is_school_admin') and user.is_school_admin():
        certificates = TrainingCertificate.objects.filter(enrollment__user=user).order_by('-issue_date')
    else:
        certificates = TrainingCertificate.objects.filter(enrollment__user=user).order_by('-issue_date')
    return render(request, "training/certificate_list.html", {'certificates': certificates})

@login_required
def certificate_detail_view(request, certificate_id):
    certificate = get_object_or_404(TrainingCertificate, certificate_id=certificate_id)
    user = request.user
    if not (user.is_reb_officer() or user.is_system_admin() or certificate.enrollment.user == user):
        return HttpResponseForbidden()
    return render(request, "training/certificate_detail.html", {'certificate': certificate})

@login_required
def certificate_edit_view(request, certificate_id):
    certificate = get_object_or_404(TrainingCertificate, certificate_id=certificate_id)
    user = request.user
    if not (user.is_reb_officer() or user.is_system_admin() or (user.is_school_admin() and certificate.created_by == user)):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = TrainingCertificateForm(request.POST, request.FILES, instance=certificate)
        if form.is_valid():
            form.save()
            return redirect('training:certificate_detail', certificate_id=certificate.certificate_id)
    else:
        form = TrainingCertificateForm(instance=certificate)
    return render(request, "training/certificate_edit.html", {'form': form, 'certificate': certificate})

@login_required
def certificate_delete_view(request, certificate_id):
    certificate = get_object_or_404(TrainingCertificate, certificate_id=certificate_id)
    user = request.user
    if not (user.is_reb_officer() or user.is_system_admin() or (user.is_school_admin() and certificate.created_by == user)):
        return HttpResponseForbidden()
    if request.method == 'POST':
        certificate.delete()
        return redirect('training:certificate_list')
    return render(request, "training/certificate_delete.html", {'certificate': certificate})

def certificate_download_view(request, certificate_id):
    return render(request, "training/certificate_download.html")

def calendar_view(request):
    """Display the training calendar page with session data."""
    sessions = TrainingSession.objects.filter(status='scheduled')
    events = [
        {
            'title': s.session_title,
            'start': s.start_date.isoformat(),
            'end': s.end_date.isoformat() if s.end_date else s.start_date.isoformat(),
            'id': str(s.session_id),
            'course': s.course.course_title,
        }
        for s in sessions
    ]
    return render(request, "training/calendar.html", {
        'events_json': json.dumps(events, cls=DjangoJSONEncoder)
    })
