from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from collections import Counter

from .models import User, School, SchoolUser, District, SystemConfiguration
from grants.models import GrantProposal, GrantCategory
from budget.models import SchoolBudget, BudgetPeriod
from training.models import TrainingCourse, TrainingEnrollment
from community.models import CommunityForum, Announcement
from .forms import SchoolForm
from ai_engine.models import ProposalPrediction, ProposalAnomaly, AIModelStatus
from .forms import UserCreateForm


def login_view(request):
    """User login view."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'core/login.html')


def logout_view(request):
    """User logout view."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('core:login')


def register_view(request):
    """User registration view with role-based creation restrictions."""
    allowed_roles = []
    user = request.user if request.user.is_authenticated else None
    # Determine allowed roles
    if user and user.is_authenticated:
        if user.is_system_admin():
            allowed_roles = [r[0] for r in User.ROLE_CHOICES]
        elif user.is_reb_officer():
            allowed_roles = ['school_admin', 'teacher', 'community_member']
        elif user.is_school_admin():
            allowed_roles = ['teacher', 'community_member']
        else:
            allowed_roles = []
    else:
        # Public registration: only allow teacher or community_member
        allowed_roles = ['teacher', 'community_member']

    role_choices = User.ROLE_CHOICES

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role', 'teacher')

        if role not in allowed_roles:
            messages.error(request, 'You do not have permission to create this user role.')
            return render(request, 'core/register.html', {'allowed_roles': allowed_roles, 'role_choices': role_choices})

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'core/register.html', {'allowed_roles': allowed_roles, 'role_choices': role_choices})

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'core/register.html', {'allowed_roles': allowed_roles, 'role_choices': role_choices})

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'core/register.html', {'allowed_roles': allowed_roles, 'role_choices': role_choices})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            role=role,
            status='pending'
        )

        messages.success(request, 'Registration successful! Please wait for approval.')
        return redirect('core:login')

    return render(request, 'core/register.html', {'allowed_roles': allowed_roles, 'role_choices': role_choices})


def home_view(request):
    """Public landing page for GrantTracker."""
    return render(request, 'home.html')


@login_required
def dashboard_view(request):
    """Main dashboard view with role-based content."""
    user = request.user
    
    # Get user's school assignments
    school_assignments = SchoolUser.objects.filter(
        user=user, 
        is_active=True
    ).select_related('school')
    
    # Get basic statistics
    context = {
        'user': user,
        'school_assignments': school_assignments,
        'current_date': timezone.now(),
    }
    
    # Add role-specific data
    if user.is_reb_officer():
        context.update(get_reb_officer_dashboard_data())
    elif user.is_school_admin():
        context.update(get_school_admin_dashboard_data(user))
    elif user.is_teacher():
        context.update(get_teacher_dashboard_data(user))
    elif user.is_community_member():
        context.update(get_community_dashboard_data(user))
    elif user.is_system_admin():
        context.update(get_system_admin_dashboard_data())

    # --- Always include these stats for all users ---
    context['total_proposals'] = GrantProposal.objects.count()
    context['pending_proposals'] = GrantProposal.objects.filter(status='submitted').count()
    context['total_budget_allocated'] = GrantProposal.objects.filter(status__in=['approved', 'funded']).aggregate(total=Sum('allocated_amount'))['total'] or 0

    # --- Dynamic Data for Charts and Metrics ---
    # Proposals by status
    status_counts = dict(GrantProposal.objects.values_list('status').annotate(count=Count('id')))
    # Budget allocation by district
    district_budgets = School.objects.values('district').annotate(total=Sum('grant_proposals__allocated_amount')).order_by('-total')[:7]
    district_labels = [d['district'] for d in district_budgets]
    district_totals = [float(d['total'] or 0) for d in district_budgets]
    # Proposals per month (last 6 months)
    now = timezone.now()
    months = [(now - timedelta(days=30*i)).strftime('%b %Y') for i in range(5, -1, -1)]
    month_counts = []
    for m in months:
        month, year = m.split(' ')
        count = GrantProposal.objects.filter(created_at__year=int(year), created_at__month=datetime.strptime(month, '%b').month).count()
        month_counts.append(count)
    # Completion rate
    total = GrantProposal.objects.count()
    completed = GrantProposal.objects.filter(status='completed').count()
    completion_rate = (completed / total * 100) if total else 0
    # Most funded district
    most_funded = district_labels[0] if district_labels else None
    # Average grant size
    avg_grant = GrantProposal.objects.aggregate(avg=Avg('allocated_amount'))['avg'] or 0
    context.update({
        'status_counts': status_counts,
        'district_labels': district_labels,
        'district_totals': district_totals,
        'months': months,
        'month_counts': month_counts,
        'completion_rate': completion_rate,
        'most_funded': most_funded,
        'avg_grant': avg_grant,
    })
    
    # --- AI Statistics and Charts ---
    ai_predictions = ProposalPrediction.objects.all()
    ai_anomalies = ProposalAnomaly.objects.all()
    ai_status = AIModelStatus.objects.filter(component='prediction').first()
    ai_accuracy = ai_status.accuracy * 100 if ai_status else 0
    total_predictions = ai_predictions.count()
    total_anomalies = ai_anomalies.count()
    avg_pred_score = ai_predictions.aggregate(avg=Avg('score'))['avg'] or 0
    anomaly_rate = (total_anomalies / total_predictions * 100) if total_predictions else 0
    # Score distribution
    ai_score_list = list(ai_predictions.values_list('score', flat=True))
    # Anomaly frequency by month
    anomaly_dates = [a.detected_at.strftime('%Y-%m') for a in ai_anomalies]
    anomaly_counts = Counter(anomaly_dates)
    anomaly_months = sorted(anomaly_counts.keys())
    anomaly_freq = [anomaly_counts[m] for m in anomaly_months]
    # Top 5 proposals by AI score
    top_pred_objs = ai_predictions.order_by('-score')[:5]
    top_titles = [p.proposal.proposal_title for p in top_pred_objs]
    top_scores = [p.score for p in top_pred_objs]
    context.update({
        'ai_accuracy': ai_accuracy,
        'ai_total_predictions': total_predictions,
        'ai_total_anomalies': total_anomalies,
        'ai_avg_pred_score': avg_pred_score,
        'ai_anomaly_rate': anomaly_rate,
        'ai_score_list': ai_score_list,
        'ai_anomaly_months': anomaly_months,
        'ai_anomaly_freq': anomaly_freq,
        'ai_top_titles': top_titles,
        'ai_top_scores': top_scores,
    })
    
    return render(request, 'core/dashboard.html', context)


def get_reb_officer_dashboard_data():
    """Get data for REB Officer dashboard."""
    today = timezone.now().date()
    last_month = today - timedelta(days=30)
    
    return {
        'total_schools': School.objects.filter(status='active').count(),
        'total_proposals': GrantProposal.objects.count(),
        'pending_proposals': GrantProposal.objects.filter(status='submitted').count(),
        'approved_proposals': GrantProposal.objects.filter(status='approved').count(),
        'total_budget_allocated': GrantProposal.objects.filter(
            status__in=['approved', 'funded']
        ).aggregate(total=Sum('allocated_amount'))['total'] or 0,
        'recent_proposals': GrantProposal.objects.filter(
            created_at__gte=last_month
        ).order_by('-created_at')[:5],
        'schools_by_district': School.objects.values('district').annotate(
            count=Count('id')
        ).order_by('-count')[:10],
    }


def get_school_admin_dashboard_data(user):
    """Get data for School Administrator dashboard."""
    school_assignments = SchoolUser.objects.filter(
        user=user, 
        is_active=True
    ).select_related('school')
    
    schools = [assignment.school for assignment in school_assignments]
    
    return {
        'schools': schools,
        'total_proposals': GrantProposal.objects.filter(school__in=schools).count(),
        'active_proposals': GrantProposal.objects.filter(
            school__in=schools,
            status__in=['submitted', 'under_review', 'approved']
        ).count(),
        'total_budget': SchoolBudget.objects.filter(school__in=schools).aggregate(
            total=Sum('total_budget_amount')
        )['total'] or 0,
        'recent_proposals': GrantProposal.objects.filter(
            school__in=schools
        ).order_by('-created_at')[:5],
    }


def get_teacher_dashboard_data(user):
    """Get data for Teacher dashboard."""
    school_assignments = SchoolUser.objects.filter(
        user=user, 
        is_active=True
    ).select_related('school')
    
    schools = [assignment.school for assignment in school_assignments]
    
    return {
        'schools': schools,
        'enrolled_courses': TrainingEnrollment.objects.filter(
            user=user,
            status__in=['enrolled', 'in_progress']
        ).select_related('course')[:5],
        'recent_announcements': Announcement.objects.filter(
            is_active=True,
            publish_date__lte=timezone.now()
        ).order_by('-publish_date')[:3],
    }


def get_community_dashboard_data(user):
    """Get data for Community Member dashboard."""
    return {
        'recent_announcements': Announcement.objects.filter(
            is_active=True,
            publish_date__lte=timezone.now()
        ).order_by('-publish_date')[:5],
        'active_forums': CommunityForum.objects.filter(
            is_active=True
        ).order_by('-total_posts')[:5],
    }


def get_system_admin_dashboard_data():
    """Get data for System Administrator dashboard."""
    return {
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(status='active').count(),
        'total_schools': School.objects.count(),
        'system_health': {
            'database_size': '2.5 GB',
            'uptime': '99.8%',
            'active_sessions': 45,
        }
    }


@login_required
def role_dashboard_view(request, role):
    """Role-specific dashboard view."""
    user = request.user
    
    # Check if user has permission to access this role dashboard
    if not hasattr(user, f'is_{role}') or not getattr(user, f'is_{role}')():
        messages.error(request, 'You do not have permission to access this dashboard.')
        return redirect('core:dashboard')
    
    context = {
        'user': user,
        'role': role,
    }
    
    # Add role-specific data
    if role == 'reb_officer':
        context.update(get_reb_officer_dashboard_data())
        template = 'core/dashboards/reb_officer.html'
    elif role == 'school_admin':
        context.update(get_school_admin_dashboard_data(user))
        template = 'core/dashboards/school_admin.html'
    elif role == 'teacher':
        context.update(get_teacher_dashboard_data(user))
        template = 'core/dashboards/teacher.html'
    elif role == 'community_member':
        context.update(get_community_dashboard_data(user))
        template = 'core/dashboards/community.html'
    elif role == 'system_admin':
        context.update(get_system_admin_dashboard_data())
        template = 'core/dashboards/system_admin.html'
    else:
        messages.error(request, 'Invalid role specified.')
        return redirect('core:dashboard')
    
    return render(request, template, context)


@login_required
def profile_view(request):
    """User profile view."""
    user = request.user
    school_assignments = SchoolUser.objects.filter(
        user=user, 
        is_active=True
    ).select_related('school')
    
    context = {
        'user': user,
        'school_assignments': school_assignments,
    }
    
    return render(request, 'core/profile.html', context)


@login_required
def profile_edit_view(request):
    """User profile edit view."""
    user = request.user
    
    if request.method == 'POST':
        # Handle profile update
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.address = request.POST.get('address', user.address)
        
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('core:profile')
    
    return render(request, 'core/profile_edit.html', {'user': user})


@login_required
@user_passes_test(lambda u: u.is_reb_officer() or u.is_system_admin())
def school_list_view(request):
    """School list view for REB officers and system admins."""
    schools = School.objects.filter(status='active').order_by('school_name')
    
    # Add search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        schools = schools.filter(
            school_name__icontains=search_query
        ) | schools.filter(
            school_code__icontains=search_query
        ) | schools.filter(
            district__icontains=search_query
        )
    
    context = {
        'schools': schools,
        'search_query': search_query,
    }
    
    return render(request, 'core/school_list.html', context)


@login_required
def school_detail_view(request, school_id):
    """School detail view."""
    school = get_object_or_404(School, school_id=school_id)
    
    # Check if user has access to this school
    user = request.user
    if not (user.is_reb_officer() or user.is_system_admin()):
        school_access = SchoolUser.objects.filter(
            user=user,
            school=school,
            is_active=True
        ).exists()
        if not school_access:
            messages.error(request, 'You do not have access to this school.')
            return redirect('core:dashboard')
    
    # Get school statistics
    context = {
        'school': school,
        'total_proposals': GrantProposal.objects.filter(school=school).count(),
        'active_proposals': GrantProposal.objects.filter(
            school=school,
            status__in=['submitted', 'under_review', 'approved']
        ).count(),
        'total_budget': SchoolBudget.objects.filter(school=school).aggregate(
            total=Sum('total_budget_amount')
        )['total'] or 0,
        'recent_proposals': GrantProposal.objects.filter(
            school=school
        ).order_by('-created_at')[:5],
    }
    
    return render(request, 'core/school_detail.html', context)


@login_required
@user_passes_test(lambda u: u.is_reb_officer() or u.is_system_admin())
def school_edit_view(request, school_id):
    """School edit view."""
    school = get_object_or_404(School, school_id=school_id)
    
    if request.method == 'POST':
        # Handle school update
        school.school_name = request.POST.get('school_name', school.school_name)
        school.district = request.POST.get('district', school.district)
        school.sector = request.POST.get('sector', school.sector)
        school.cell = request.POST.get('cell', school.cell)
        school.village = request.POST.get('village', school.village)
        school.address = request.POST.get('address', school.address)
        school.phone_number = request.POST.get('phone_number', school.phone_number)
        school.email_address = request.POST.get('email_address', school.email_address)
        school.principal_name = request.POST.get('principal_name', school.principal_name)
        school.principal_phone = request.POST.get('principal_phone', school.principal_phone)
        school.principal_email = request.POST.get('principal_email', school.principal_email)
        
        school.save()
        messages.success(request, 'School updated successfully!')
        return redirect('core:school_detail', school_id=school.school_id)
    
    return render(request, 'core/school_edit.html', {'school': school})


@login_required
@user_passes_test(lambda u: u.is_reb_officer() or u.is_system_admin() or u.is_superuser)
def user_list_view(request):
    """User list view for REB officers and system admins."""
    users = User.objects.all().order_by('-created_at')
    
    # Add search and filter functionality
    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')
    status_filter = request.GET.get('status', '')
    
    if search_query:
        users = users.filter(
            username__icontains=search_query
        ) | users.filter(
            first_name__icontains=search_query
        ) | users.filter(
            last_name__icontains=search_query
        ) | users.filter(
            email__icontains=search_query
        )
    
    if role_filter:
        users = users.filter(role=role_filter)
    
    if status_filter:
        users = users.filter(status=status_filter)
    
    context = {
        'users': users,
        'search_query': search_query,
        'role_filter': role_filter,
        'status_filter': status_filter,
    }
    
    return render(request, 'core/user_list.html', context)


@login_required
@user_passes_test(lambda u: u.is_reb_officer() or u.is_system_admin() or u.is_superuser)
def user_detail_view(request, user_id):
    """User detail view."""
    user_detail = get_object_or_404(User, user_id=user_id)
    
    context = {
        'user_detail': user_detail,
        'school_assignments': SchoolUser.objects.filter(
            user=user_detail
        ).select_related('school'),
    }
    
    return render(request, 'core/user_detail.html', context)


@login_required
@user_passes_test(lambda u: u.is_reb_officer() or u.is_system_admin() or u.is_superuser)
def user_edit_view(request, user_id):
    """User edit view."""
    user_detail = get_object_or_404(User, user_id=user_id)
    
    if request.method == 'POST':
        # Handle user update
        user_detail.first_name = request.POST.get('first_name', user_detail.first_name)
        user_detail.last_name = request.POST.get('last_name', user_detail.last_name)
        user_detail.email = request.POST.get('email', user_detail.email)
        user_detail.role = request.POST.get('role', user_detail.role)
        user_detail.status = request.POST.get('status', user_detail.status)
        user_detail.phone_number = request.POST.get('phone_number', user_detail.phone_number)
        
        user_detail.save()
        messages.success(request, 'User updated successfully!')
        return redirect('core:user_detail', user_id=user_detail.user_id)
    
    return render(request, 'core/user_edit.html', {'user_detail': user_detail})


@login_required
@user_passes_test(lambda u: u.is_reb_officer() or u.is_system_admin() or u.is_superuser)
def user_create_view(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully!')
            return redirect('core:user_list')
    else:
        form = UserCreateForm()
    return render(request, 'core/user_create.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_reb_officer() or u.is_system_admin() or u.is_superuser)
def user_activate_view(request, user_id):
    user_obj = get_object_or_404(User, user_id=user_id)
    user_obj.status = 'active'
    user_obj.save()
    messages.success(request, f'User {user_obj.username} activated.')
    return redirect('core:user_list')

@login_required
@user_passes_test(lambda u: u.is_reb_officer() or u.is_system_admin() or u.is_superuser)
def user_deactivate_view(request, user_id):
    user_obj = get_object_or_404(User, user_id=user_id)
    user_obj.status = 'inactive'
    user_obj.save()
    messages.success(request, f'User {user_obj.username} deactivated.')
    return redirect('core:user_list')

@login_required
@user_passes_test(lambda u: u.is_reb_officer() or u.is_system_admin() or u.is_superuser)
def user_delete_view(request, user_id):
    user_obj = get_object_or_404(User, user_id=user_id)
    username = user_obj.username
    user_obj.delete()
    messages.success(request, f'User {username} deleted.')
    return redirect('core:user_list')


@login_required
@user_passes_test(lambda u: u.is_system_admin())
def settings_view(request):
    """System settings view for system administrators."""
    return render(request, 'core/settings.html')


@login_required
@user_passes_test(lambda u: u.is_system_admin())
def system_settings_view(request):
    """System configuration view."""
    if request.method == 'POST':
        # Handle system settings update
        for key, value in request.POST.items():
            if key.startswith('config_'):
                config_key = key.replace('config_', '')
                try:
                    config = SystemConfiguration.objects.get(config_key=config_key)
                    config.config_value = value
                    config.save()
                except SystemConfiguration.DoesNotExist:
                    pass
        
        messages.success(request, 'System settings updated successfully!')
        return redirect('core:system_settings')
    
    configurations = SystemConfiguration.objects.filter(is_active=True).order_by('category', 'config_key')
    
    context = {
        'configurations': configurations,
    }
    
    return render(request, 'core/system_settings.html', context)


@login_required
@user_passes_test(lambda u: u.is_system_admin())
def school_create_view(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            school = form.save(commit=False)
            school.created_by = request.user
            school.save()
            messages.success(request, 'School created successfully!')
            return redirect('core:school_list')
    else:
        form = SchoolForm()
    return render(request, 'core/school_form.html', {'form': form, 'action': 'Create'})


def custom_404(request, exception=None):
    """Custom 404 error page."""
    return render(request, 'core/404.html', status=404)


def custom_500(request):
    """Custom 500 error page."""
    return render(request, 'core/500.html', status=500)
