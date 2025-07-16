from django.shortcuts import render
from django.http import HttpResponse
from reporting.models import Report, KPI, KPIValue
from grants.models import GrantProposal
from django.db.models import Sum, Avg, F, DurationField, ExpressionWrapper, Count, Q
from django.db.models.functions import ExtractYear
from django.template.loader import render_to_string, get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.utils import timezone
from budget.models import BudgetReport
import json
from core.models import School
from ai_engine.ml_pipeline import predict, extract_features_from_ocr
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django import forms
import pandas as pd
from django.template.loader import render_to_string
from collections import defaultdict
from .models import REBGrantBudget
try:
    from xhtml2pdf import pisa
except ImportError:
    pisa = None
from django.urls import reverse
from .forms import REBGrantBudgetForm
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.

def dashboard_overview_view(request):
    # Dynamic statistics
    total_reports = Report.objects.count()
    approved_proposals = GrantProposal.objects.filter(status='approved').count()
    total_funding = GrantProposal.objects.filter(status='approved').aggregate(total=Sum('requested_amount'))['total'] or 0
    total_proposals = GrantProposal.objects.count()
    success_rate = int((approved_proposals / total_proposals) * 100) if total_proposals else 0

    # Recent reports
    recent_reports = Report.objects.order_by('-created_at')[:3]

    # --- Performance Chart Data (Proposals Submitted/Approved per Month) ---
    from collections import OrderedDict
    import calendar
    now = timezone.now()
    months = [(now.replace(month=m, day=1)).strftime('%b') for m in range(1, 13)]
    submitted_per_month = [0]*12
    approved_per_month = [0]*12
    proposals = GrantProposal.objects.all()
    for p in proposals:
        m = p.created_at.month - 1
        submitted_per_month[m] += 1
        if p.status == 'approved':
            approved_per_month[m] += 1

    # --- Funding Distribution by District ---
    district_funding = GrantProposal.objects.filter(status='approved').values('school__district').annotate(
        total=Sum('requested_amount')).order_by('-total')
    district_labels = [row['school__district'] or 'Unknown' for row in district_funding]
    district_data = [float(row['total'] or 0) for row in district_funding]

    # --- Key Metrics ---
    avg_grant_size = GrantProposal.objects.filter(status='approved').aggregate(avg=Avg('requested_amount'))['avg'] or 0
    # Processing time: average days from created_at to approval_date (if available)
    proposals_with_approval = GrantProposal.objects.filter(status='approved').exclude(approval_date=None)
    if proposals_with_approval.exists():
        avg_processing_time = proposals_with_approval.annotate(
            proc_time=ExpressionWrapper(F('approval_date') - F('created_at'), output_field=DurationField())
        ).aggregate(avg=Avg('proc_time'))['avg']
        avg_processing_days = int(avg_processing_time.days) if avg_processing_time else 0
    else:
        avg_processing_days = 0
    # Completion rate: percent of proposals with status 'completed' or 'closed'
    completed_count = GrantProposal.objects.filter(status__in=['completed', 'closed']).count()
    completion_rate = int((completed_count / total_proposals) * 100) if total_proposals else 0

    # --- Additional Key Metrics ---
    total_schools = School.objects.count()
    # Most funded district
    most_funded = district_funding[0]['school__district'] if district_funding else 'N/A'
    most_funded_amount = district_funding[0]['total'] if district_funding else 0

    context = {
        'total_reports': total_reports,
        'approved_proposals': approved_proposals,
        'total_funding': total_funding,
        'success_rate': success_rate,
        'recent_reports': recent_reports,
        # Chart data as JSON
        'performance_labels_json': json.dumps(months),
        'performance_submitted_json': json.dumps(submitted_per_month),
        'performance_approved_json': json.dumps(approved_per_month),
        'district_labels_json': json.dumps(district_labels),
        'district_data_json': json.dumps(district_data),
        # Key metrics
        'avg_grant_size': int(avg_grant_size),
        'avg_processing_days': avg_processing_days,
        'completion_rate': completion_rate,
        'total_schools': total_schools,
        'most_funded_district': most_funded,
        'most_funded_amount': int(most_funded_amount),
    }
    return render(request, "reporting/overview.html", context)

def dashboard_list_view(request):
    return render(request, "reporting/dashboard_list.html")

def dashboard_create_view(request):
    return render(request, "reporting/dashboard_create.html")

def dashboard_detail_view(request, dashboard_id):
    return render(request, "reporting/dashboard_detail.html")

def dashboard_edit_view(request, dashboard_id):
    return render(request, "reporting/dashboard_edit.html")

def widget_list_view(request, dashboard_id):
    return render(request, "reporting/widget_list.html")

def widget_add_view(request, dashboard_id):
    return render(request, "reporting/widget_add.html")

def widget_detail_view(request, widget_id):
    return render(request, "reporting/widget_detail.html")

def widget_edit_view(request, widget_id):
    return render(request, "reporting/widget_edit.html")

def widget_delete_view(request, widget_id):
    return render(request, "reporting/widget_delete.html")

def kpi_list_view(request):
    return render(request, "reporting/kpi_list.html")

def kpi_create_view(request):
    return render(request, "reporting/kpi_create.html")

def kpi_detail_view(request, kpi_id):
    return render(request, "reporting/kpi_detail.html")

def kpi_edit_view(request, kpi_id):
    return render(request, "reporting/kpi_edit.html")

def kpi_values_view(request, kpi_id):
    return render(request, "reporting/kpi_values.html")

def report_list_view(request):
    return render(request, "reporting/report_list.html")

def report_create_view(request):
    return render(request, "reporting/report_create.html")

def report_detail_view(request, report_id):
    return render(request, "reporting/report_detail.html")

def report_generate_view(request, report_id):
    return render(request, "reporting/report_generate.html")

def report_download_view(request, report_id):
    return render(request, "reporting/report_download.html")

def schedule_list_view(request):
    return render(request, "reporting/schedule_list.html")

def schedule_create_view(request):
    return render(request, "reporting/schedule_create.html")

def schedule_detail_view(request, schedule_id):
    return render(request, "reporting/schedule_detail.html")

def schedule_edit_view(request, schedule_id):
    return render(request, "reporting/schedule_edit.html")

def analytics_overview_view(request):
    return render(request, "reporting/analytics_overview.html")

def analytics_events_view(request):
    return render(request, "reporting/analytics_events.html")

def analytics_users_view(request):
    return render(request, "reporting/analytics_users.html")

def analytics_performance_view(request):
    return render(request, "reporting/analytics_performance.html")

def export_list_view(request):
    return render(request, "reporting/export_list.html")

def export_create_view(request):
    return render(request, "reporting/export_create.html")

def export_detail_view(request, export_id):
    return render(request, "reporting/export_detail.html")

def export_download_view(request, export_id):
    return render(request, "reporting/export_download.html")

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return result.getvalue()
    return None

def generate_template_report(request, template_type):
    context = {
        'user': request.user,
        'now': timezone.now(),
    }
    if template_type == 'monthly':
        context['budget_reports'] = BudgetReport.objects.filter(report_type='monthly')
        context['kpis'] = KPI.objects.all()
        context['kpi_values'] = KPIValue.objects.all()
        template_name = 'reporting/monthly_report_pdf.html'
        filename = 'monthly_report.pdf'
    elif template_type == 'performance':
        context['kpis'] = KPI.objects.all()
        context['kpi_values'] = KPIValue.objects.all()
        template_name = 'reporting/performance_report_pdf.html'
        filename = 'performance_report.pdf'
    elif template_type == 'financial':
        context['reports'] = Report.objects.filter(report_type='financial_report')
        context['budget_reports'] = BudgetReport.objects.all()
        template_name = 'reporting/financial_report_pdf.html'
        filename = 'financial_report.pdf'
    elif template_type == 'school':
        context['reports'] = Report.objects.filter(report_type='school_performance')
        context['budget_reports'] = BudgetReport.objects.all()
        template_name = 'reporting/school_report_pdf.html'
        filename = 'school_report.pdf'
    elif template_type == 'custom':
        context['reports'] = Report.objects.filter(report_type='custom')
        template_name = 'reporting/custom_report_pdf.html'
        filename = 'custom_report.pdf'
    elif template_type == 'executive_summary':
        context['report_type'] = 'Executive Summary'
        context['description'] = 'High-level overview for senior management'
        context['reports'] = Report.objects.all()[:10]
        context['budget_reports'] = BudgetReport.objects.all()[:5]
        context['kpis'] = KPI.objects.all()[:5]
        context['kpi_values'] = KPIValue.objects.all()[:10]
        template_name = 'reporting/custom_report_pdf.html'
        filename = 'executive_summary.pdf'
    elif template_type == 'financial_analysis':
        context['report_type'] = 'Financial Analysis'
        context['description'] = 'Detailed financial breakdown and trends'
        context['reports'] = Report.objects.filter(report_type='financial_report')
        context['budget_reports'] = BudgetReport.objects.all()
        template_name = 'reporting/financial_report_pdf.html'
        filename = 'financial_analysis.pdf'
    elif template_type == 'performance_metrics':
        context['report_type'] = 'Performance Metrics'
        context['description'] = 'KPI tracking and performance indicators'
        context['kpis'] = KPI.objects.all()
        context['kpi_values'] = KPIValue.objects.all()
        template_name = 'reporting/performance_report_pdf.html'
        filename = 'performance_metrics.pdf'
    else:
        context.update({'report_type': 'Unknown', 'description': 'Unknown report template'})
        return render(request, 'reporting/report_generate.html', context)

    pdf = render_to_pdf(template_name, context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        return HttpResponse('Error generating PDF', status=500)

class GrantAllocationForm(forms.Form):
    total_amount = forms.DecimalField(
        label='Total Available Grant',
        min_value=0,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter total grant amount'})
    )

@login_required
@user_passes_test(lambda u: u.is_system_admin() or u.is_reb_officer())
def school_grant_totals_view(request):
    schools = School.objects.filter(status='active').order_by('school_name')
    school_data = []
    total_predicted_sum = 0
    for school in schools:
        proposals = school.grant_proposals.exclude(status__in=['rejected', 'completed', 'closed'])
        total_proposed = proposals.aggregate(total=Sum('requested_amount'))['total'] or 0
        total_predicted = 0
        for proposal in proposals:
            ocr_texts = [doc.ocr_text for doc in proposal.documents.all() if doc.ocr_text]
            full_ocr_text = "\n".join(ocr_texts)
            if not full_ocr_text and proposal.description:
                full_ocr_text = proposal.description
            if full_ocr_text:
                features = {'requested_amount': proposal.requested_amount}
                features.update(extract_features_from_ocr(full_ocr_text))
                try:
                    predicted = predict(features)
                except Exception:
                    predicted = 0
                total_predicted += predicted
        school_data.append({
            'school': school,
            'total_proposed': total_proposed,
            'total_predicted': total_predicted,
        })
        total_predicted_sum += total_predicted

    allocated = False
    total_amount = None
    if request.method == 'POST':
        form = GrantAllocationForm(request.POST)
        if form.is_valid():
            total_amount = form.cleaned_data['total_amount']
            allocated = True
            # Proportional allocation
            for row in school_data:
                if total_predicted_sum > 0:
                    row['ai_allocated'] = (row['total_predicted'] / total_predicted_sum) * float(total_amount)
                else:
                    row['ai_allocated'] = 0
    else:
        form = GrantAllocationForm()
        for row in school_data:
            row['ai_allocated'] = None

    context = {
        'school_data': school_data,
        'form': form,
        'allocated': allocated,
        'total_amount': total_amount,
    }
    return render(request, 'reporting/school_grant_totals.html', context)

@login_required
@user_passes_test(lambda u: u.is_reb_officer() or u.is_system_admin())
def reb_budget_planning_view(request):
    # Get the latest REB grant budget (by year)
    budget = REBGrantBudget.objects.order_by('-year', '-created_at').first()
    total_grant = budget.total_amount if budget else 0
    year = budget.year if budget else None
    notes = budget.notes if budget else ''
    # Total granted (allocated)
    total_granted = GrantProposal.objects.aggregate(total=Sum('allocated_amount'))['total'] or 0
    remaining = total_grant - total_granted
    context = {
        'budget': budget,
        'total_grant': total_grant,
        'total_granted': total_granted,
        'remaining': remaining,
        'year': year,
        'notes': notes,
    }
    return render(request, 'reporting/reb_budget_planning.html', context)

@login_required
@user_passes_test(lambda u: u.is_reb_officer() or u.is_system_admin())
def reb_budget_edit_view(request):
    # If year is provided as GET param, try to edit that year, else use latest or blank
    year = request.GET.get('year')
    if year:
        budget = REBGrantBudget.objects.filter(year=year).first()
    else:
        budget = REBGrantBudget.objects.order_by('-year', '-created_at').first()
    if request.method == 'POST':
        form = REBGrantBudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, 'REB Grant Budget saved successfully.')
            return redirect('reporting:reb_budget_planning')
    else:
        form = REBGrantBudgetForm(instance=budget)
    return render(request, 'reporting/reb_budget_edit.html', {'form': form, 'budget': budget})

@login_required
@user_passes_test(lambda u: u.is_reb_officer() or u.is_system_admin())
def annual_grant_report_view(request):
    proposals = GrantProposal.objects.exclude(created_at__isnull=True)
    grants_by_year = defaultdict(lambda: {
        'year': None,
        'total_grants': 0,
        'total_amount': 0,
        'submitted': 0,
        'approved': 0,
        'funded': 0,
        'rejected': 0,
    })
    debug_info = []
    for p in proposals:
        year = str(p.created_at.year) if p.created_at else 'Unknown'
        debug_info.append(f'Proposal ID: {p.id}, created_at: {p.created_at}, extracted year: {year}')
        row = grants_by_year[year]
        row['year'] = year
        row['total_grants'] += 1
        row['total_amount'] += float(p.allocated_amount or 0)
        if p.status == 'submitted':
            row['submitted'] += 1
        if p.status == 'approved':
            row['approved'] += 1
        if p.status == 'funded':
            row['funded'] += 1
        if p.status == 'rejected':
            row['rejected'] += 1
    grants_by_year_list = sorted(grants_by_year.values(), key=lambda x: x['year'], reverse=True)
    print('\n'.join(debug_info))
    return render(request, 'reporting/annual_grant_report.html', {'grants_by_year': grants_by_year_list})

@login_required
@user_passes_test(lambda u: u.is_reb_officer() or u.is_system_admin())
def annual_grant_report_export_view(request, format):
    proposals = GrantProposal.objects.exclude(created_at__isnull=True)
    grants_by_year = defaultdict(lambda: {
        'year': None,
        'total_grants': 0,
        'total_amount': 0,
        'submitted': 0,
        'approved': 0,
        'funded': 0,
        'rejected': 0,
    })
    for p in proposals:
        year = str(p.created_at.year) if p.created_at else 'Unknown'
        row = grants_by_year[year]
        row['year'] = year
        row['total_grants'] += 1
        row['total_amount'] += float(p.allocated_amount or 0)
        if p.status == 'submitted':
            row['submitted'] += 1
        if p.status == 'approved':
            row['approved'] += 1
        if p.status == 'funded':
            row['funded'] += 1
        if p.status == 'rejected':
            row['rejected'] += 1
    data = sorted(grants_by_year.values(), key=lambda x: x['year'], reverse=True)
    if format == 'excel':
        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=annual_grant_report.xlsx'
        df.to_excel(response, index=False)
        return response
    elif format == 'pdf' and pisa:
        html = render_to_string('reporting/annual_grant_report_export.html', {'grants_by_year': data})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=annual_grant_report.pdf'
        pisa.CreatePDF(html, dest=response)
        return response
    else:
        return HttpResponse('Export format not supported or PDF export requires xhtml2pdf.', status=400)

@login_required
@user_passes_test(lambda u: u.is_reb_officer() or u.is_system_admin())
def reb_budget_planning_export_excel(request):
    budget = REBGrantBudget.objects.order_by('-year', '-created_at').first()
    total_grant = budget.total_amount if budget else 0
    year = budget.year if budget else None
    notes = budget.notes if budget else ''
    total_granted = GrantProposal.objects.aggregate(total=Sum('allocated_amount'))['total'] or 0
    remaining = total_grant - total_granted
    data = [{
        'Year': year,
        'Total Grant': total_grant,
        'Total Granted': total_granted,
        'Remaining': remaining,
        'Notes': notes,
    }]
    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=reb_budget_planning.xlsx'
    df.to_excel(response, index=False)
    return response

@login_required
@user_passes_test(lambda u: u.is_reb_officer() or u.is_system_admin())
def reb_budget_planning_export_pdf(request):
    budget = REBGrantBudget.objects.order_by('-year', '-created_at').first()
    total_grant = budget.total_amount if budget else 0
    year = budget.year if budget else None
    notes = budget.notes if budget else ''
    total_granted = GrantProposal.objects.aggregate(total=Sum('allocated_amount'))['total'] or 0
    remaining = total_grant - total_granted
    context = {
        'budget': budget,
        'total_grant': total_grant,
        'total_granted': total_granted,
        'remaining': remaining,
        'year': year,
        'notes': notes,
    }
    html = render_to_string('reporting/reb_budget_planning_export.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=reb_budget_planning.pdf'
    pisa.CreatePDF(html, dest=response)
    return response
