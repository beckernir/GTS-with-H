from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden, FileResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import GrantProposal, GrantCategory
from .forms import GrantProposalForm, GrantCategoryForm
from core.models import AuditLog
import csv
import openpyxl
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.contrib import messages
from django.utils import timezone
import pytesseract
from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
from PyPDF2 import PdfReader
from ai_engine.ml_pipeline import predict, extract_features_from_ocr
from reporting.models import ProposalCriterion
from reporting.models import ProposalCriterionResponse
from .forms import GrantProposalWithCriteriaForm

# Create your views here.

def get_proposal_score(proposal):
    features = {
        'requested_amount': proposal.requested_amount or 0,
        # Add more static features as needed
    }
    # Add dynamic criteria responses
    for response in proposal.criterion_responses.all():
        if response.criterion.type == 'text':
            features[f'criterion_{response.criterion.id}_text'] = response.value_text or ''
        elif response.criterion.type == 'boolean':
            features[f'criterion_{response.criterion.id}_bool'] = int(response.value_bool) if response.value_bool is not None else 0
        elif response.criterion.type == 'file' and response.value_file:
            # Optionally use OCR or file metadata
            try:
                ocr_text = response.value_file.read().decode(errors='ignore') if hasattr(response.value_file, 'read') else ''
            except Exception:
                ocr_text = ''
            features.update(extract_features_from_ocr(ocr_text))
    try:
        score = predict(features)
    except Exception:
        score = 0
    return score

def proposal_list_view(request):
    """Display a list of all grant proposals."""
    user = request.user
    if user.is_authenticated:
        if hasattr(user, 'is_reb_officer') and (user.is_reb_officer() or user.is_system_admin()):
            proposals = GrantProposal.objects.all().order_by('-created_at')
        elif hasattr(user, 'is_school_admin') and user.is_school_admin():
            proposals = GrantProposal.objects.filter(school__user_assignments__user=user).order_by('-created_at')
        elif hasattr(user, 'is_teacher') and user.is_teacher():
            proposals = GrantProposal.objects.filter(created_by=user).order_by('-created_at')
        else:
            proposals = GrantProposal.objects.none()
    else:
        proposals = GrantProposal.objects.none()
    categories = GrantCategory.objects.filter(is_active=True)
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        proposals = proposals.filter(status=status_filter)
    
    # Filter by category if provided
    category_filter = request.GET.get('category')
    if category_filter:
        proposals = proposals.filter(grant_category_id=category_filter)
    
    # ML scoring and sorting
    proposal_scores = [(p, get_proposal_score(p)) for p in proposals]
    if proposal_scores:
        min_score = min(s for _, s in proposal_scores)
        max_score = max(s for _, s in proposal_scores)
        if min_score == max_score:
            min_score = 0  # avoid division by zero
        for p, score in proposal_scores:
            if max_score > min_score:
                norm_score = (score - min_score) / (max_score - min_score) * 99.9
                p.ml_score = '{:.1f}'.format(norm_score)
            else:
                p.ml_score = '99.9'
    else:
        for p, _ in proposal_scores:
            p.ml_score = '0.0'
    proposal_scores.sort(key=lambda x: float(x[0].ml_score), reverse=True)
    context = {
        'proposals': [p for p, s in proposal_scores],
        'categories': categories,
        'status_choices': GrantProposal.STATUS_CHOICES,
        'current_status': status_filter,
        'current_category': category_filter,
    }
    return render(request, "grants/proposal_list.html", context)

@login_required
@user_passes_test(lambda u: (hasattr(u, 'is_school_admin') and u.is_school_admin()) or (hasattr(u, 'is_system_admin') and (u.is_system_admin if isinstance(u.is_system_admin, bool) else u.is_system_admin())))
def proposal_create_view(request):
    if request.method == 'POST':
        form = GrantProposalWithCriteriaForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.created_by = request.user
            proposal.status = 'submitted'
            if hasattr(request.user, 'is_system_admin') and (
                request.user.is_system_admin if isinstance(request.user.is_system_admin, bool) else request.user.is_system_admin()
            ):
                proposal.school = form.cleaned_data['school']
            else:
                from datetime import date
                from django.db.models import Q
                print("User:", request.user)
                print("Assignments:", list(request.user.school_assignments.all()))
                school_assignment = request.user.school_assignments.filter(
                    is_active=True,
                    start_date__lte=date.today()
                ).filter(
                    Q(end_date__isnull=True) | Q(end_date__gte=date.today())
                ).first()
                print("Filtered assignment:", school_assignment)
                if school_assignment:
                    proposal.school = school_assignment.school
                else:
                    form.add_error(None, 'You are not assigned to any active school. Please contact the administrator.')
                    return render(request, "grants/proposal_create.html", {'form': form, 'is_system_admin': False})
            if not proposal.school:
                form.add_error('school', 'School is required.')
                return render(request, "grants/proposal_create.html", {'form': form, 'is_system_admin': request.user.is_system_admin()})
            proposal.save()
            # Save criterion responses
            for field_name, field in form.fields.items():
                if hasattr(field, 'criterion_obj'):
                    criterion = field.criterion_obj
                    value = form.cleaned_data.get(field_name)
                    response_kwargs = {'proposal': proposal, 'criterion': criterion}
                    if criterion.type == 'file':
                        if value:
                            obj, created = ProposalCriterionResponse.objects.update_or_create(
                                **response_kwargs,
                                defaults={'value_file': value, 'value_text': None, 'value_bool': None}
                            )
                            if not created and value:
                                obj.value_file = value
                                obj.save()
                    elif criterion.type == 'text':
                        ProposalCriterionResponse.objects.update_or_create(
                            **response_kwargs,
                            defaults={'value_text': value, 'value_file': None, 'value_bool': None}
                        )
                    elif criterion.type == 'boolean':
                        ProposalCriterionResponse.objects.update_or_create(
                            **response_kwargs,
                            defaults={'value_bool': value, 'value_file': None, 'value_text': None}
                        )
            return redirect('grants:proposal_list')
    else:
        form = GrantProposalWithCriteriaForm(user=request.user)
    is_system_admin = hasattr(request.user, 'is_system_admin') and (
        request.user.is_system_admin if isinstance(request.user.is_system_admin, bool) else request.user.is_system_admin()
    )
    return render(request, "grants/proposal_create.html", {'form': form, 'is_system_admin': is_system_admin})

def proposal_detail_view(request, proposal_id):
    """Display detailed information about a specific grant proposal."""
    proposal = get_object_or_404(GrantProposal, proposal_id=proposal_id)
    
    context = {
        'proposal': proposal,
        'budget_items': proposal.budget_items.all(),
        'documents': proposal.documents.all(),
        'allocations': proposal.fund_allocations.all(),
        'reviews': proposal.reviews.all(),
    }
    # ML Recommendation logic
    recommended_amount = None
    # Aggregate OCR text from all related documents
    ocr_texts = [doc.ocr_text for doc in proposal.documents.all() if doc.ocr_text]
    full_ocr_text = "\n".join(ocr_texts)
    # If no document OCR, use proposal description
    if not full_ocr_text and proposal.description:
        full_ocr_text = proposal.description
    if full_ocr_text:
        features = {
            'requested_amount': proposal.requested_amount,
            # Add other structured features as needed
        }
        features.update(extract_features_from_ocr(full_ocr_text))
        try:
            recommended_amount = predict(features)
        except Exception:
            recommended_amount = None
    context['recommended_amount'] = recommended_amount
    return render(request, "grants/proposal_detail.html", context)

@login_required
def proposal_edit_view(request, proposal_id):
    proposal = get_object_or_404(GrantProposal, proposal_id=proposal_id)
    user = request.user
    if not (user.is_reb_officer() or user.is_system_admin() or (user.is_school_admin() and proposal.school in [a.school for a in user.school_assignments.filter(is_active=True)])):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = GrantProposalForm(request.POST, instance=proposal)
        if form.is_valid():
            form.save()
            return redirect('grants:proposal_detail', proposal_id=proposal.proposal_id)
    else:
        form = GrantProposalForm(instance=proposal)
    return render(request, "grants/proposal_edit.html", {'form': form, 'proposal': proposal})

@login_required
def proposal_submit_view(request, proposal_id):
    proposal = get_object_or_404(GrantProposal, proposal_id=proposal_id)
    if proposal.status not in ['draft']:
        messages.warning(request, 'Proposal has already been submitted or is not in draft status.')
        return redirect('grants:proposal_detail', proposal_id=proposal.proposal_id)
    proposal.status = 'submitted'
    proposal.submission_date = timezone.now()
    proposal.save()
    messages.success(request, 'Proposal submitted for review!')
    return redirect('grants:proposal_detail', proposal_id=proposal.proposal_id)

@login_required
def proposal_delete_view(request, proposal_id):
    proposal = get_object_or_404(GrantProposal, proposal_id=proposal_id)
    user = request.user
    if not (user.is_reb_officer() or user.is_system_admin() or (user.is_school_admin() and proposal.school in [a.school for a in user.school_assignments.filter(is_active=True)])):
        return HttpResponseForbidden()
    if request.method == 'POST':
        proposal.delete()
        return redirect('grants:proposal_list')
    return render(request, "grants/proposal_delete.html", {'proposal': proposal})

def can_manage_categories(user):
    return (
        (hasattr(user, 'is_system_admin') and (user.is_system_admin if isinstance(user.is_system_admin, bool) else user.is_system_admin())) or
        (hasattr(user, 'is_reb_officer') and (user.is_reb_officer if isinstance(user.is_reb_officer, bool) else user.is_reb_officer()))
    )

@login_required
@user_passes_test(can_manage_categories)
def category_list_view(request):
    categories = GrantCategory.objects.all().order_by('category_name')
    return render(request, 'grants/category_list.html', {'categories': categories})

@login_required
@user_passes_test(can_manage_categories)
def category_create_view(request):
    if request.method == 'POST':
        form = GrantCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            # Audit log
            AuditLog.objects.create(
                user=request.user,
                action='create',
                object_type='GrantCategory',
                object_id=str(category.id),
                object_repr=str(category)
            )
            return redirect('grants:category_list')
    else:
        form = GrantCategoryForm()
    return render(request, 'grants/category_form.html', {'form': form, 'action': 'Create'})

@login_required
@user_passes_test(can_manage_categories)
def category_edit_view(request, category_id):
    category = get_object_or_404(GrantCategory, category_id=category_id)
    if request.method == 'POST':
        form = GrantCategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            # Audit log
            AuditLog.objects.create(
                user=request.user,
                action='update',
                object_type='GrantCategory',
                object_id=str(category.id),
                object_repr=str(category)
            )
            return redirect('grants:category_list')
    else:
        form = GrantCategoryForm(instance=category)
    return render(request, 'grants/category_form.html', {'form': form, 'action': 'Edit'})

@login_required
@user_passes_test(can_manage_categories)
def category_delete_view(request, category_id):
    category = get_object_or_404(GrantCategory, category_id=category_id)
    if request.method == 'POST':
        # Audit log before delete
        AuditLog.objects.create(
            user=request.user,
            action='delete',
            object_type='GrantCategory',
            object_id=str(category.id),
            object_repr=str(category)
        )
        category.delete()
        return redirect('grants:category_list')
    return render(request, 'grants/category_confirm_delete.html', {'category': category})

def category_detail_view(request, category_id):
    return render(request, "grants/category_detail.html")

def document_list_view(request, proposal_id):
    return render(request, "grants/document_list.html")

def document_upload_view(request, proposal_id):
    proposal = get_object_or_404(GrantProposal, proposal_id=proposal_id)
    if request.method == 'POST':
        # ... get uploaded file ...
        uploaded_file = request.FILES.get('document_file')
        ocr_text = None
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
                image = Image.open(uploaded_file)
                ocr_text = pytesseract.image_to_string(image)
            elif ext == '.pdf':
                pdf_reader = PdfReader(uploaded_file)
                text = []
                for page in pdf_reader.pages:
                    text.append(page.extract_text() or '')
                ocr_text = '\n'.join(text)
            # Save ProposalDocument with ocr_text
            # ... create ProposalDocument instance ...
            doc = ProposalDocument.objects.create(
                proposal=proposal,
                document_type=document_type,
                document_title=document_title,
                document_file=uploaded_file,
                file_size=uploaded_file.size,
                description=description,
                uploaded_by=request.user,
                ocr_text=ocr_text
            )
            messages.success(request, 'Document uploaded successfully. OCR analysis complete.' if ocr_text else 'Document uploaded successfully.')
            return redirect('grants:document_list', proposal_id=proposal_id)
    # ... existing code ...

def document_detail_view(request, document_id):
    from .models import ProposalDocument
    document = get_object_or_404(ProposalDocument, document_id=document_id)
    return render(request, "grants/document_detail.html", {"document": document})

def document_delete_view(request, document_id):
    return render(request, "grants/document_delete.html")

def budget_view(request, proposal_id):
    return render(request, "grants/budget_view.html")

def budget_item_add_view(request, proposal_id):
    return render(request, "grants/budget_item_add.html")

def budget_item_edit_view(request, proposal_id, item_id):
    return render(request, "grants/budget_item_edit.html")

def budget_item_delete_view(request, proposal_id, item_id):
    return render(request, "grants/budget_item_delete.html")

def allocation_view(request, proposal_id):
    return render(request, "grants/allocation_view.html")

def allocation_create_view(request, proposal_id):
    return render(request, "grants/allocation_create.html")

def review_view(request, proposal_id):
    return render(request, "grants/review_view.html")

def review_create_view(request, proposal_id):
    return render(request, "grants/review_create.html")

def ai_allocation_view(request):
    return render(request, "grants/ai_allocation.html")

def ai_allocation_run_view(request):
    return render(request, "grants/ai_allocation_run.html")

@login_required
@user_passes_test(can_manage_categories)
def category_export_excel_view(request):
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = 'Grant Categories'
    ws.append(['Name', 'Type', 'Description', 'Min Amount', 'Max Amount', 'Priority Weight', 'Active'])
    for cat in GrantCategory.objects.all():
        ws.append([
            cat.category_name,
            cat.category_type,
            cat.description,
            cat.min_amount,
            cat.max_amount,
            cat.priority_weight,
            'Yes' if cat.is_active else 'No',
        ])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=grant_categories.xlsx'
    wb.save(response)
    return response

@login_required
@user_passes_test(can_manage_categories)
def category_export_pdf_view(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 40
    p.setFont('Helvetica-Bold', 14)
    p.drawString(40, y, 'Grant Categories')
    y -= 30
    p.setFont('Helvetica-Bold', 10)
    headers = ['Name', 'Type', 'Description', 'Min Amount', 'Max Amount', 'Priority Weight', 'Active']
    for i, h in enumerate(headers):
        p.drawString(40 + i*90, y, h)
    y -= 20
    p.setFont('Helvetica', 10)
    for cat in GrantCategory.objects.all():
        row = [
            cat.category_name,
            cat.category_type,
            cat.description,
            str(cat.min_amount),
            str(cat.max_amount),
            str(cat.priority_weight),
            'Yes' if cat.is_active else 'No',
        ]
        for i, val in enumerate(row):
            p.drawString(40 + i*90, y, val[:15])
        y -= 18
        if y < 40:
            p.showPage()
            y = height - 40
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='grant_categories.pdf')

@login_required
@user_passes_test(lambda u: u.is_reb_officer() or u.is_system_admin())
def proposal_approve_view(request, proposal_id):
    proposal = get_object_or_404(GrantProposal, proposal_id=proposal_id)
    if proposal.status not in ['submitted', 'under_review']:
        messages.warning(request, 'Only submitted or under review proposals can be approved.')
        return redirect('grants:proposal_detail', proposal_id=proposal_id)
    proposal.status = 'approved'
    proposal.approval_date = timezone.now()
    proposal.save()
    messages.success(request, 'Proposal approved successfully!')
    return redirect('grants:proposal_detail', proposal_id=proposal_id)

@login_required
@user_passes_test(lambda u: u.is_reb_officer() or u.is_system_admin())
def proposal_reject_view(request, proposal_id):
    proposal = get_object_or_404(GrantProposal, proposal_id=proposal_id)
    if proposal.status not in ['submitted', 'under_review']:
        messages.warning(request, 'Only submitted or under review proposals can be rejected.')
        return redirect('grants:proposal_detail', proposal_id=proposal_id)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', '')
        proposal.status = 'rejected'
        proposal.rejection_reason = reason
        proposal.save()
        messages.success(request, 'Proposal rejected successfully!')
        return redirect('grants:proposal_detail', proposal_id=proposal_id)
    return render(request, 'grants/proposal_reject.html', {'proposal': proposal})

@login_required
def proposal_review_view(request, proposal_id):
    proposal = get_object_or_404(GrantProposal, proposal_id=proposal_id)
    # Placeholder: Add review logic here as needed
    return render(request, 'grants/proposal_review.html', {'proposal': proposal})

@login_required
def proposal_allocate_view(request, proposal_id):
    proposal = get_object_or_404(GrantProposal, proposal_id=proposal_id)
    # Placeholder: Add allocation logic here as needed
    return render(request, 'grants/proposal_allocate.html', {'proposal': proposal}) 