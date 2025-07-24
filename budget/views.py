from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import SchoolBudget, BudgetLineItem, BudgetPeriod, BudgetCategory, BudgetTransfer
from .forms import SchoolBudgetForm, BudgetLineItemForm, BudgetPeriodForm, BudgetTransferForm
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_POST
from core.models import School
import csv
from reportlab.pdfgen import canvas
from io import BytesIO
from openpyxl import Workbook
from django.utils import timezone
from django.db import models
from django.db.models import Q

# Create your views here.

def budget_overview_view(request):
    # Summary cards
    total_budget = SchoolBudget.objects.aggregate(total=models.Sum('total_budget_amount'))['total'] or 0
    allocated_budget = SchoolBudget.objects.aggregate(allocated=models.Sum('allocated_amount'))['allocated'] or 0
    pending_budget = SchoolBudget.objects.filter(status='submitted').aggregate(pending=models.Sum('total_budget_amount'))['pending'] or 0
    remaining_budget = allocated_budget - SchoolBudget.objects.aggregate(spent=models.Sum('spent_amount'))['spent'] or 0

    # Recent allocations (last 5)
    recent_allocations = SchoolBudget.objects.select_related('school').order_by('-created_at')[:5]

    # Budget alerts (dummy for now)
    budget_alerts = []
    if allocated_budget > 0 and remaining_budget / allocated_budget < 0.1:
        budget_alerts.append({'level': 'danger', 'message': 'Less than 10% of allocated budget remaining!'})
    if pending_budget > 0:
        budget_alerts.append({'level': 'warning', 'message': 'There are budgets pending approval.'})

    # Category breakdown for table/chart
    categories = BudgetCategory.objects.all()
    category_data = []
    for cat in categories:
        total = SchoolBudget.objects.filter(line_items__budget_category=cat).aggregate(total=models.Sum('total_budget_amount'))['total'] or 0
        allocated = BudgetLineItem.objects.filter(budget_category=cat).aggregate(allocated=models.Sum('allocated_amount'))['allocated'] or 0
        spent = BudgetLineItem.objects.filter(budget_category=cat).aggregate(spent=models.Sum('spent_amount'))['spent'] or 0
        remaining = allocated - spent
        utilization = (spent / allocated * 100) if allocated else 0
        category_data.append({
            'category': cat.category_name,
            'category_id': str(cat.category_id),
            'total': total,
            'allocated': allocated,
            'spent': spent,
            'remaining': remaining,
            'utilization': utilization,
        })

    print('DEBUG: category_data:', category_data)
    print('DEBUG: recent_allocations:', list(recent_allocations))

    return render(request, "budget/overview.html", {
        'total_budget': total_budget,
        'allocated_budget': allocated_budget,
        'pending_budget': pending_budget,
        'remaining_budget': remaining_budget,
        'recent_allocations': recent_allocations,
        'budget_alerts': budget_alerts,
        'category_data': category_data,
    })

def period_list_view(request):
    periods = BudgetPeriod.objects.all().order_by('-start_date')
    total_periods = periods.count()
    active_periods = periods.filter(is_active=True).count()
    closed_periods = periods.filter(is_closed=True).count()
    draft_periods = periods.filter(is_active=False, is_closed=False).count()
    total_budget_sum = sum([p.total_budget_limit for p in periods])
    return render(request, "budget/period_list.html", {
        'periods': periods,
        'total_periods': total_periods,
        'active_periods': active_periods,
        'closed_periods': closed_periods,
        'draft_periods': draft_periods,
        'total_budget_sum': total_budget_sum,
    })

def is_admin_or_reb(user):
    return (hasattr(user, 'is_system_admin') and user.is_system_admin()) or (hasattr(user, 'is_reb_officer') and user.is_reb_officer())

@login_required
@user_passes_test(is_admin_or_reb)
def period_create_view(request):
    if request.method == 'POST':
        form = BudgetPeriodForm(request.POST)
        if form.is_valid():
            period = form.save(commit=False)
            period.created_by = request.user
            period.save()
            messages.success(request, 'Budget period created successfully.')
            return redirect(reverse('budget:period_list'))
    else:
        form = BudgetPeriodForm()
    return render(request, "budget/period_create.html", {'form': form})

def period_detail_view(request, period_id):
    period = get_object_or_404(BudgetPeriod, period_id=period_id)
    return render(request, "budget/period_detail.html", {'period': period})

def period_edit_view(request, period_id):
    period = get_object_or_404(BudgetPeriod, period_id=period_id)
    if request.method == 'POST':
        form = BudgetPeriodForm(request.POST, instance=period)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget period updated successfully.')
            return redirect('budget:period_detail', period_id=period.period_id)
    else:
        form = BudgetPeriodForm(instance=period)
    return render(request, "budget/period_edit.html", {'form': form, 'period': period})

@login_required
@user_passes_test(is_admin_or_reb)
def period_delete_view(request, period_id):
    period = get_object_or_404(BudgetPeriod, period_id=period_id)
    if request.method == 'POST':
        period.delete()
        messages.success(request, 'Budget period deleted successfully.')
        return redirect('budget:period_list')
    return render(request, 'budget/period_delete.html', {'period': period})

# List school budgets with role-based filtering
@login_required
def school_budget_list_view(request):
    user = request.user
    if hasattr(user, 'is_reb_officer') and (user.is_reb_officer() or user.is_system_admin()):
        budgets = SchoolBudget.objects.all().order_by('-created_at')
    elif hasattr(user, 'is_school_admin') and user.is_school_admin():
        budgets = SchoolBudget.objects.filter(
            Q(school__user_assignments__user=user) | Q(created_by=user)
        ).distinct().order_by('-created_at')
    else:
        budgets = SchoolBudget.objects.none()
    total_schools = budgets.values('school').distinct().count()
    approved_budgets = budgets.filter(status='approved').count()
    pending_budgets = budgets.filter(status='submitted').count()
    total_budget_sum = sum([b.total_budget_amount for b in budgets])
    assigned_school_ids = []
    if hasattr(user, 'is_school_admin') and user.is_school_admin():
        assigned_school_ids = list(user.school_assignments.filter(is_active=True).values_list('school_id', flat=True))
    return render(request, "budget/school_budget_list.html", {
        'budgets': budgets,
        'total_schools': total_schools,
        'approved_budgets': approved_budgets,
        'pending_budgets': pending_budgets,
        'total_budget_sum': total_budget_sum,
        'assigned_school_ids': assigned_school_ids,
    })

# Create school budget
@login_required
def school_budget_create_view(request):
    user = request.user
    is_sys_admin = hasattr(user, 'is_system_admin') and user.is_system_admin()
    if request.method == 'POST':
        form = SchoolBudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.created_by = user
            if not is_sys_admin:
                school_assignment = user.school_assignments.filter(is_active=True).first()
                if school_assignment:
                    budget.school = school_assignment.school
            budget.save()
            return redirect('budget:school_budget_list')
    else:
        form = SchoolBudgetForm()
    return render(request, "budget/school_budget_create.html", {'form': form, 'is_sys_admin': is_sys_admin})

def school_budget_detail_view(request, budget_id):
    budget = get_object_or_404(SchoolBudget, budget_id=budget_id)
    user = request.user
    user_can_edit = False
    if hasattr(user, 'is_system_admin') and user.is_system_admin():
        user_can_edit = True
    elif hasattr(user, 'is_reb_officer') and user.is_reb_officer():
        user_can_edit = True
    elif hasattr(user, 'is_school_admin') and user.is_school_admin():
        assigned_school_ids = list(user.school_assignments.filter(is_active=True).values_list('school_id', flat=True))
        if budget.school.id in assigned_school_ids:
            user_can_edit = True
    # Summary card data (same as list view)
    if hasattr(user, 'is_reb_officer') and (user.is_reb_officer() or user.is_system_admin()):
        budgets = SchoolBudget.objects.all()
    elif hasattr(user, 'is_school_admin') and user.is_school_admin():
        budgets = SchoolBudget.objects.filter(school__user_assignments__user=user)
    else:
        budgets = SchoolBudget.objects.none()
    total_schools = budgets.values('school').distinct().count()
    approved_budgets = budgets.filter(status='approved').count()
    pending_budgets = budgets.filter(status='submitted').count()
    total_budget_sum = sum([b.total_budget_amount for b in budgets])
    return render(request, "budget/school_budget_detail.html", {
        'budget': budget,
        'user_can_edit': user_can_edit,
        'total_schools': total_schools,
        'approved_budgets': approved_budgets,
        'pending_budgets': pending_budgets,
        'total_budget_amount': total_budget_sum,
    })

# Edit school budget
@login_required
def school_budget_edit_view(request, budget_id):
    budget = get_object_or_404(SchoolBudget, budget_id=budget_id)
    user = request.user
    is_sys_admin = hasattr(user, 'is_system_admin') and user.is_system_admin()
    if not (user.is_reb_officer() or user.is_system_admin() or (user.is_school_admin() and budget.school in [a.school for a in user.school_assignments.filter(is_active=True)])):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = SchoolBudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('budget:school_budget_detail', budget_id=budget.budget_id)
    else:
        form = SchoolBudgetForm(instance=budget)
    return render(request, "budget/school_budget_edit.html", {'form': form, 'budget': budget, 'is_sys_admin': is_sys_admin})

def category_list_view(request):
    return render(request, "budget/category_list.html")

def category_detail_view(request, category_id):
    category = get_object_or_404(BudgetCategory, category_id=category_id)
    return render(request, "budget/category_detail.html", {"category": category})

def line_item_list_view(request, budget_id):
    return render(request, "budget/line_item_list.html")

# Add budget line item
@login_required
def line_item_add_view(request, budget_id):
    budget = get_object_or_404(SchoolBudget, budget_id=budget_id)
    user = request.user
    if not (user.is_reb_officer() or user.is_system_admin() or (user.is_school_admin() and budget.school in [a.school for a in user.school_assignments.filter(is_active=True)])):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = BudgetLineItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.school_budget = budget
            item.created_by = user
            item.save()
            return redirect('budget:line_item_list', budget_id=budget.budget_id)
    else:
        form = BudgetLineItemForm()
    return render(request, "budget/line_item_add.html", {'form': form, 'budget': budget})

def line_item_detail_view(request, item_id):
    return render(request, "budget/line_item_detail.html")

# Edit budget line item
@login_required
def line_item_edit_view(request, item_id):
    item = get_object_or_404(BudgetLineItem, line_item_id=item_id)
    user = request.user
    if not (user.is_reb_officer() or user.is_system_admin() or (user.is_school_admin() and item.school_budget.school in [a.school for a in user.school_assignments.filter(is_active=True)])):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = BudgetLineItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('budget:line_item_list', budget_id=item.school_budget.budget_id)
    else:
        form = BudgetLineItemForm(instance=item)
    return render(request, "budget/line_item_edit.html", {'form': form, 'item': item})

# Delete budget line item
@login_required
def line_item_delete_view(request, item_id):
    item = get_object_or_404(BudgetLineItem, line_item_id=item_id)
    user = request.user
    if not (user.is_reb_officer() or user.is_system_admin() or (user.is_school_admin() and item.school_budget.school in [a.school for a in user.school_assignments.filter(is_active=True)])):
        return HttpResponseForbidden()
    budget_id = item.school_budget.budget_id
    if request.method == 'POST':
        item.delete()
        return redirect('budget:line_item_list', budget_id=budget_id)
    return render(request, "budget/line_item_delete.html", {'item': item})

def expenditure_list_view(request, item_id):
    return render(request, "budget/expenditure_list.html")

def expenditure_add_view(request, item_id):
    return render(request, "budget/expenditure_add.html")

def expenditure_detail_view(request, expenditure_id):
    return render(request, "budget/expenditure_detail.html")

def expenditure_edit_view(request, expenditure_id):
    return render(request, "budget/expenditure_edit.html")

def expenditure_delete_view(request, expenditure_id):
    return render(request, "budget/expenditure_delete.html")

def transfer_list_view(request):
    user = request.user
    # Show all transfers for admins/REB, or only relevant ones for school admins
    if hasattr(user, 'is_reb_officer') and (user.is_reb_officer() or user.is_system_admin()):
        transfers = BudgetTransfer.objects.select_related('source_line_item__school_budget__school', 'destination_line_item__school_budget__school', 'source_line_item__budget_category').all().order_by('-transfer_date')
    elif hasattr(user, 'is_school_admin') and user.is_school_admin():
        school_ids = user.school_assignments.filter(is_active=True).values_list('school_id', flat=True)
        transfers = BudgetTransfer.objects.filter(
            source_line_item__school_budget__school__in=school_ids
        ).select_related('source_line_item__school_budget__school', 'destination_line_item__school_budget__school', 'source_line_item__budget_category').order_by('-transfer_date')
    else:
        transfers = BudgetTransfer.objects.none()
    total_transfers = transfers.count()
    approved = transfers.filter(is_approved=True).count()
    pending = transfers.filter(is_approved=False).count()
    total_amount = sum([t.transfer_amount for t in transfers])
    return render(request, "budget/transfer_list.html", {
        'transfers': transfers,
        'total_transfers': total_transfers,
        'approved': approved,
        'pending': pending,
        'total_amount': total_amount,
    })

@login_required
def transfer_create_view(request):
    user = request.user
    if not (hasattr(user, 'is_school_admin') and user.is_school_admin()) and \
       not (hasattr(user, 'is_reb_officer') and user.is_reb_officer()) and \
       not (hasattr(user, 'is_system_admin') and user.is_system_admin()):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = BudgetTransferForm(request.POST)
        if form.is_valid():
            transfer = form.save(commit=False)
            transfer.created_by = user
            transfer.save()
            return redirect('budget:transfer_list')
    else:
        form = BudgetTransferForm()
    return render(request, "budget/transfer_create.html", {"form": form})

def transfer_detail_view(request, transfer_id):
    transfer = get_object_or_404(BudgetTransfer, transfer_id=transfer_id)
    user = request.user
    user_can_approve = (hasattr(user, 'is_reb_officer') and user.is_reb_officer()) or (hasattr(user, 'is_system_admin') and user.is_system_admin())
    return render(request, "budget/transfer_detail.html", {"transfer": transfer, "user_can_approve": user_can_approve})

def transfer_approve_view(request, transfer_id):
    transfer = get_object_or_404(BudgetTransfer, transfer_id=transfer_id)
    if request.method == 'POST':
        transfer.is_approved = True
        transfer.approval_date = timezone.now()
        transfer.approved_by = request.user
        transfer.save()
        return redirect('budget:transfer_detail', transfer_id=transfer.transfer_id)
    return render(request, "budget/transfer_approve.html", {"transfer": transfer})

def report_list_view(request):
    return render(request, "budget/report_list.html")

@login_required
def report_generate_view(request):
    user = request.user
    if not (hasattr(user, 'is_school_admin') and user.is_school_admin()) and \
       not (hasattr(user, 'is_reb_officer') and user.is_reb_officer()) and \
       not (hasattr(user, 'is_system_admin') and user.is_system_admin()):
        return HttpResponse("You are not authorized to generate budget reports.", status=403)

    schools = School.objects.filter(status='active').order_by('school_name')
    categories = BudgetCategory.objects.filter(is_active=True).order_by('category_name')

    if request.method == 'POST':
        report_type = request.POST.get('report_type')
        period = request.POST.get('period')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        school_id = request.POST.get('school')
        category_id = request.POST.get('category')
        output_format = request.POST.get('format')
        include_charts = request.POST.get('include_charts') == 'on'
        include_details = request.POST.get('include_details') == 'on'

        # CSV file download
        if output_format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="budget_report.csv"'
            writer = csv.writer(response)
            writer.writerow(['School', 'Category', 'Budget Amount'])
            writer.writerow(['School A', 'Instructional Materials', '1000000'])
            writer.writerow(['School B', 'Infrastructure', '2000000'])
            writer.writerow(['School C', 'Staffing', '1500000'])
            return response
        # Excel file download
        if output_format == 'excel':
            wb = Workbook()
            ws = wb.active
            ws.title = "Budget Report"
            ws.append(['School', 'Category', 'Budget Amount'])
            ws.append(['School A', 'Instructional Materials', '1000000'])
            ws.append(['School B', 'Infrastructure', '2000000'])
            ws.append(['School C', 'Staffing', '1500000'])
            excel_buffer = BytesIO()
            wb.save(excel_buffer)
            excel_buffer.seek(0)
            response = HttpResponse(excel_buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="budget_report.xlsx"'
            return response
        # Example: Generate a PDF file with dummy data
        if output_format == 'pdf':
            buffer = BytesIO()
            p = canvas.Canvas(buffer)
            p.setFont("Helvetica-Bold", 16)
            p.drawString(100, 800, "Budget Report")
            p.setFont("Helvetica", 12)
            p.drawString(100, 770, f"Report Type: {report_type}")
            p.drawString(100, 750, f"Period: {period}")
            p.drawString(100, 730, f"Date Range: {start_date} - {end_date}")
            p.drawString(100, 710, f"School ID: {school_id}")
            p.drawString(100, 690, f"Category ID: {category_id}")
            p.drawString(100, 670, f"Include Charts: {include_charts}")
            p.drawString(100, 650, f"Include Details: {include_details}")
            p.showPage()
            p.save()
            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="budget_report.pdf"'
            return response
        # TODO: Add Excel generation here
        return HttpResponse(f"Report generated: {report_type}, {period}, {start_date} - {end_date}, school={school_id}, category={category_id}, format={output_format}, charts={include_charts}, details={include_details}")

    return render(request, "budget/report_generate.html", {
        'schools': schools,
        'categories': categories,
    })

def report_detail_view(request, report_id):
    return render(request, "budget/report_detail.html")

def report_download_view(request, report_id):
    return render(request, "budget/report_download.html")

@login_required
def school_budget_delete_view(request, budget_id):
    budget = get_object_or_404(SchoolBudget, budget_id=budget_id)
    user = request.user
    if not (user.is_reb_officer() or user.is_system_admin() or (user.is_school_admin() and budget.school in [a.school for a in user.school_assignments.filter(is_active=True)])):
        return HttpResponseForbidden()
    if request.method == 'POST':
        budget.delete()
        messages.success(request, 'School budget deleted successfully.')
        return redirect('budget:school_budget_list')
    return render(request, 'budget/school_budget_delete.html', {'budget': budget})
