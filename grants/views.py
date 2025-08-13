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
try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False
from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
from PyPDF2 import PdfReader
from ai_engine.ml_pipeline import predict, extract_features_from_ocr
from reporting.models import ProposalCriterion
from reporting.models import ProposalCriterionResponse
from .forms import GrantProposalWithCriteriaForm
from core.models import School
from .models import TotalGrantAllocation
from .forms import TotalGrantAllocationForm

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
                if hasattr(response.value_file, 'read'):
                    file_content = response.value_file.read()
                    if isinstance(file_content, bytes):
                        try:
                            ocr_text = file_content.decode('utf-8', errors='ignore')
                        except UnicodeDecodeError:
                            ocr_text = file_content.decode('latin-1', errors='ignore')
                    else:
                        ocr_text = str(file_content)
                else:
                    ocr_text = ''
            except Exception as e:
                print(f"Error reading file content: {e}")
                ocr_text = ''
            features.update(extract_features_from_ocr(ocr_text))
    try:
        score = predict(features)
    except Exception as e:
        print(f"Error predicting score: {e}")
        score = 0
    return score

def proposal_list_view(request):
    """Display a list of all grant proposals."""
    user = request.user
    selected_school_id = request.GET.get('school')
    
    # Filter schools based on user permissions
    if user.is_authenticated:
        if hasattr(user, 'is_reb_officer') and (user.is_reb_officer() or user.is_system_admin()):
            # REB officers and system admins can see all schools
            schools = School.objects.filter(status='active').order_by('school_name')
            proposals = GrantProposal.objects.all().order_by('-created_at')
        elif hasattr(user, 'is_school_admin') and user.is_school_admin():
            # School admins can only see their assigned schools
            user_schools = School.objects.filter(
                user_assignments__user=user,
                user_assignments__is_active=True
            ).distinct()
            schools = user_schools.order_by('school_name')
            
            # School admins can only see proposals from their assigned schools
            from django.db.models import Q
            proposals = GrantProposal.objects.filter(
                Q(school__in=user_schools) | Q(created_by=user)
            ).distinct().order_by('-created_at')
            
            # Ignore any school filter parameter for school admins - they only see their schools
            selected_school_id = None
            
        elif hasattr(user, 'is_teacher') and user.is_teacher():
            # Teachers can only see their own proposals
            schools = School.objects.filter(
                user_assignments__user=user,
                user_assignments__is_active=True
            ).distinct().order_by('school_name')
            proposals = GrantProposal.objects.filter(created_by=user).order_by('-created_at')
        else:
            schools = School.objects.none()
            proposals = GrantProposal.objects.none()
    else:
        schools = School.objects.none()
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
    proposal_scores = []
    for p in proposals:
        try:
            score = get_proposal_score(p)
            proposal_scores.append((p, score))
        except Exception as e:
            print(f"Error getting score for proposal {p.proposal_id}: {e}")
            proposal_scores.append((p, 0))
    if proposal_scores:
        try:
            min_score = min(s for _, s in proposal_scores)
            max_score = max(s for _, s in proposal_scores)
            if min_score == max_score:
                min_score = 0  # avoid division by zero
        except Exception as e:
            print(f"Error calculating min/max scores: {e}")
            min_score = 0
            max_score = 1
        for p, score in proposal_scores:
            try:
                if max_score > min_score:
                    norm_score = (score - min_score) / (max_score - min_score) * 99.9
                    p.ml_score = '{:.1f}'.format(norm_score)
                else:
                    p.ml_score = '99.9'
            except Exception as e:
                print(f"Error calculating ml_score for proposal {p.proposal_id}: {e}")
                p.ml_score = '0.0'
    else:
        # No proposals to score
        pass
    try:
        proposal_scores.sort(key=lambda x: float(x[0].ml_score), reverse=True)
    except Exception as e:
        print(f"Error sorting proposals: {e}")
        # Keep original order if sorting fails
    context = {
        'proposals': [p for p, s in proposal_scores],
        'categories': categories,
        'status_choices': GrantProposal.STATUS_CHOICES,
        'current_status': status_filter,
        'current_category': category_filter,
        'schools': schools,
        'selected_school_id': selected_school_id,
    }
    return render(request, "grants/proposal_list.html", context)

@login_required
@user_passes_test(lambda u: hasattr(u, 'is_school_admin') and u.is_school_admin())
def proposal_create_view(request):
    if request.method == 'POST':
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
        form = GrantProposalWithCriteriaForm(request.POST, request.FILES, user=request.user, school_instance=school_assignment.school if 'school_assignment' in locals() and school_assignment else None)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.created_by = request.user
            proposal.status = 'submitted'
            
            # Automatically calculate requested_amount from form-only fields
            total_amount = form.cleaned_data.get('total_amount', 0)
            current_amount = form.cleaned_data.get('current_amount', 0)
            proposal.requested_amount = max(0, total_amount - current_amount)
            
            # For school admins, get their assigned school
            from datetime import date
            from django.db.models import Q
            school_assignment = request.user.school_assignments.filter(
                is_active=True,
                start_date__lte=date.today()
            ).filter(
                Q(end_date__isnull=True) | Q(end_date__gte=date.today())
            ).first()
            
            if school_assignment:
                proposal.school = school_assignment.school
            else:
                # No assignment: allow user to select school
                form = GrantProposalWithCriteriaForm(request.POST, request.FILES, user=request.user, force_school_field=True)
                if form.is_valid():
                    proposal = form.save(commit=False)
                    proposal.created_by = request.user
                    proposal.status = 'submitted'
                    proposal.school = form.cleaned_data['school']
                    
                    # Automatically calculate requested_amount
                    total_amount = form.cleaned_data.get('total_amount', 0)
                    current_amount = form.cleaned_data.get('current_amount', 0)
                    proposal.requested_amount = max(0, total_amount - current_amount)
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
                # If not valid, fall through to render form with errors
                return render(request, "grants/proposal_create.html", {'form': form})
            
            if not proposal.school:
                form.add_error('school', 'School is required.')
                return render(request, "grants/proposal_create.html", {'form': form})
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
            form = GrantProposalWithCriteriaForm(user=request.user, school_instance=school_assignment.school)
        else:
            # No assignment: allow user to select school
            form = GrantProposalWithCriteriaForm(user=request.user, force_school_field=True)
        
        # Debug: Print form fields
        print("Form fields:", list(form.fields.keys()))
        print("Form visible fields:", list(form.visible_fields()))
        print("Form errors:", form.errors)
        
        # Debug: Check if form has the expected fields
        print("Has total_amount:", 'total_amount' in form.fields)
        print("Has current_amount:", 'current_amount' in form.fields)
        print("Has requested_amount:", 'requested_amount' in form.fields)
        
        # Debug: Check form field types
        for field_name, field in form.fields.items():
            print(f"Field {field_name}: {type(field)}")
    return render(request, "grants/proposal_create.html", {'form': form})

@login_required
def proposal_detail_view(request, proposal_id):
    """Display detailed information about a specific grant proposal."""
    proposal = get_object_or_404(GrantProposal, proposal_id=proposal_id)
    user = request.user
    
    # Check access permissions
    if hasattr(user, 'is_system_admin') and user.is_system_admin():
        # System admins can view all proposals
        pass
    elif hasattr(user, 'is_reb_officer') and user.is_reb_officer():
        # REB officers can view all proposals
        pass
    elif hasattr(user, 'is_school_admin') and user.is_school_admin():
        # School admins can only view proposals from their assigned schools
        user_schools = School.objects.filter(
            user_assignments__user=user,
            user_assignments__is_active=True
        ).distinct()
        if proposal.school not in user_schools:
            messages.error(request, 'You do not have access to view this proposal.')
            return redirect('grants:proposal_list')
    elif hasattr(user, 'is_teacher') and user.is_teacher():
        # Teachers can only view their own proposals
        if proposal.created_by != user:
            messages.error(request, 'You can only view your own proposals.')
            return redirect('grants:proposal_list')
    else:
        # Other users cannot view proposals
        messages.error(request, 'You do not have permission to view proposals.')
        return redirect('grants:proposal_list')
    
    # Get both regular documents and criteria documents
    regular_documents = proposal.documents.all()
    criteria_documents = []
    
    # Get documents from criteria responses
    for response in proposal.criterion_responses.filter(criterion__type='file', value_file__isnull=False):
        if response.value_file:
            criteria_documents.append({
                'document_title': f"{response.criterion.name}",
                'document_type': 'supporting',
                'document_file': response.value_file,
                'uploaded_by': response.proposal.created_by,
                'uploaded_at': response.submitted_at,
                'is_criteria': True,
                'criterion_name': response.criterion.name,
            })
    
    # Combine both types of documents
    all_documents = list(regular_documents) + criteria_documents
    
    context = {
        'proposal': proposal,
        'budget_items': proposal.budget_items.all(),
        'documents': all_documents,
        'allocations': proposal.fund_allocations.all(),
        'reviews': proposal.reviews.all(),
    }
    # ML Recommendation logic
    recommended_amount = None
    try:
        # Aggregate OCR text from all related documents
        ocr_texts = []
        for doc in proposal.documents.all():
            if doc.ocr_text:
                try:
                    # Handle potential encoding issues
                    if isinstance(doc.ocr_text, bytes):
                        ocr_text = doc.ocr_text.decode('utf-8', errors='ignore')
                    else:
                        ocr_text = str(doc.ocr_text)
                    ocr_texts.append(ocr_text)
                except Exception:
                    continue
        
        full_ocr_text = "\n".join(ocr_texts)
        # If no document OCR, use proposal description
        if not full_ocr_text and proposal.description:
            full_ocr_text = str(proposal.description)
        
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
    except Exception as e:
        print(f"Error processing ML recommendation: {e}")
        recommended_amount = None
    
    context['recommended_amount'] = recommended_amount
    return render(request, "grants/proposal_detail.html", context)

@login_required
def proposal_edit_view(request, proposal_id):
    proposal = get_object_or_404(GrantProposal, proposal_id=proposal_id)
    user = request.user
    if not (user.is_school_admin() and proposal.created_by == user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = GrantProposalForm(request.POST, instance=proposal, include_status=True)
        if form.is_valid():
            form.save()
            return redirect('grants:proposal_detail', proposal_id=proposal.proposal_id)
    else:
        form = GrantProposalForm(instance=proposal, include_status=True)
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
    if not (user.is_school_admin() and proposal.created_by == user):
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
    
    # Set allocated amount to requested amount when approving
    if proposal.allocated_amount == 0:
        proposal.allocated_amount = proposal.requested_amount
        proposal.current_amount = proposal.requested_amount
    
    proposal.status = 'approved'
    proposal.approval_date = timezone.now()
    proposal.save()
    messages.success(request, 'Proposal approved successfully!')
    return redirect('grants:proposal_detail', proposal_id=proposal_id)

@login_required
@user_passes_test(lambda u: u.is_system_admin())
def proposal_fund_view(request, proposal_id):
    """Allow system administrators to mark approved proposals as funded."""
    try:
        proposal = get_object_or_404(GrantProposal, proposal_id=proposal_id)
        if proposal.status != 'approved':
            messages.warning(request, 'Only approved proposals can be marked as funded.')
            return redirect('grants:proposal_detail', proposal_id=proposal_id)
        
        if request.method == 'POST':
            # Ensure allocated amount is set when funding
            if proposal.allocated_amount == 0:
                proposal.allocated_amount = proposal.requested_amount
                proposal.current_amount = proposal.requested_amount
            
            proposal.status = 'funded'
            proposal.save()
            messages.success(request, 'Proposal marked as funded successfully!')
            return redirect('grants:proposal_detail', proposal_id=proposal_id)
        
        return render(request, 'grants/proposal_fund.html', {'proposal': proposal})
    except Exception as e:
        import traceback
        print(f"Error in proposal_fund_view: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('grants:proposal_list')

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


# Total Grant Allocation Views (System Administrator Only)

@login_required
@user_passes_test(lambda u: u.is_system_admin())
def total_grant_allocation_list_view(request):
    """
    List all total grant allocations by year for system administrators.
    """
    allocations = TotalGrantAllocation.objects.all().order_by('-fiscal_year')
    
    # Calculate summary statistics
    total_budget = sum(alloc.total_budget for alloc in allocations)
    total_allocated = sum(alloc.allocated_amount for alloc in allocations)
    total_disbursed = sum(alloc.disbursed_amount for alloc in allocations)
    
    context = {
        'allocations': allocations,
        'total_budget': total_budget,
        'total_allocated': total_allocated,
        'total_disbursed': total_disbursed,
        'total_remaining': total_budget - total_allocated,
    }
    return render(request, 'grants/total_grant_allocation_list.html', context)


@login_required
@user_passes_test(lambda u: u.is_system_admin())
def total_grant_allocation_create_view(request):
    """
    Create a new total grant allocation for a specific year.
    """
    if request.method == 'POST':
        form = TotalGrantAllocationForm(request.POST)
        if form.is_valid():
            allocation = form.save(commit=False)
            allocation.created_by = request.user
            allocation.save()
            
            messages.success(request, f'Total grant allocation for FY {allocation.fiscal_year} created successfully!')
            return redirect('grants:total_grant_allocation_list')
    else:
        form = TotalGrantAllocationForm()
    
    context = {
        'form': form,
        'title': 'Create Total Grant Allocation',
        'submit_text': 'Create Allocation',
    }
    return render(request, 'grants/total_grant_allocation_form.html', context)


@login_required
@user_passes_test(lambda u: u.is_system_admin())
def total_grant_allocation_edit_view(request, allocation_id):
    """
    Edit an existing total grant allocation.
    """
    allocation = get_object_or_404(TotalGrantAllocation, allocation_id=allocation_id)
    
    if request.method == 'POST':
        form = TotalGrantAllocationForm(request.POST, instance=allocation)
        if form.is_valid():
            allocation = form.save(commit=False)
            allocation.updated_by = request.user
            allocation.save()
            
            messages.success(request, f'Total grant allocation for FY {allocation.fiscal_year} updated successfully!')
            return redirect('grants:total_grant_allocation_list')
    else:
        form = TotalGrantAllocationForm(instance=allocation)
    
    context = {
        'form': form,
        'allocation': allocation,
        'title': f'Edit Total Grant Allocation - FY {allocation.fiscal_year}',
        'submit_text': 'Update Allocation',
    }
    return render(request, 'grants/total_grant_allocation_form.html', context)


@login_required
@user_passes_test(lambda u: u.is_system_admin())
def total_grant_allocation_detail_view(request, allocation_id):
    """
    View details of a total grant allocation.
    """
    allocation = get_object_or_404(TotalGrantAllocation, allocation_id=allocation_id)
    
    # Get related proposals for this fiscal year
    related_proposals = GrantProposal.objects.filter(
        created_at__year=allocation.fiscal_year
    ).order_by('-created_at')
    
    context = {
        'allocation': allocation,
        'related_proposals': related_proposals,
        'proposal_count': related_proposals.count(),
    }
    return render(request, 'grants/total_grant_allocation_detail.html', context)


@login_required
@user_passes_test(lambda u: u.is_system_admin())
def total_grant_allocation_delete_view(request, allocation_id):
    """
    Delete a total grant allocation.
    """
    allocation = get_object_or_404(TotalGrantAllocation, allocation_id=allocation_id)
    
    if request.method == 'POST':
        fiscal_year = allocation.fiscal_year
        allocation.delete()
        messages.success(request, f'Total grant allocation for FY {fiscal_year} deleted successfully!')
        return redirect('grants:total_grant_allocation_list')
    
    context = {
        'allocation': allocation,
    }
    return render(request, 'grants/total_grant_allocation_confirm_delete.html', context)


@login_required
@user_passes_test(lambda u: u.is_system_admin())
def total_grant_allocation_dashboard_view(request):
    """
    Dashboard view showing overview of all grant allocations.
    """
    allocations = TotalGrantAllocation.objects.all().order_by('-fiscal_year')
    
    # Calculate summary statistics
    total_budget = sum(alloc.total_budget for alloc in allocations)
    total_allocated = sum(alloc.allocated_amount for alloc in allocations)
    total_disbursed = sum(alloc.disbursed_amount for alloc in allocations)
    
    # Get current fiscal year allocation
    current_year = timezone.now().year
    current_allocation = allocations.filter(fiscal_year=current_year).first()
    
    # Get recent proposals
    recent_proposals = GrantProposal.objects.all().order_by('-created_at')[:10]
    
    context = {
        'allocations': allocations,
        'current_allocation': current_allocation,
        'recent_proposals': recent_proposals,
        'total_budget': total_budget,
        'total_allocated': total_allocated,
        'total_disbursed': total_disbursed,
        'total_remaining': total_budget - total_allocated,
        'allocation_percentage': (total_allocated / total_budget * 100) if total_budget > 0 else 0,
        'disbursement_percentage': (total_disbursed / total_budget * 100) if total_budget > 0 else 0,
    }
    return render(request, 'grants/total_grant_allocation_dashboard.html', context) 

@login_required
@user_passes_test(lambda u: u.is_reb_officer() or u.is_system_admin())
def proposal_request_changes_view(request, proposal_id):
    """Allow REB officers and system admins to request changes to proposals."""
    try:
        proposal = get_object_or_404(GrantProposal, proposal_id=proposal_id)
        
        # Only allow requesting changes for proposals that are under review or submitted
        if proposal.status not in ['submitted', 'under_review']:
            messages.warning(request, 'Only submitted or under review proposals can have changes requested.')
            return redirect('grants:proposal_detail', proposal_id=proposal_id)
        
        if request.method == 'POST':
            change_comments = request.POST.get('change_request_comments', '').strip()
            
            if not change_comments:
                messages.error(request, 'Please provide comments explaining what changes are needed.')
                return render(request, 'grants/proposal_request_changes.html', {'proposal': proposal})
            
            # Update proposal with change request
            proposal.status = 'changes_requested'
            proposal.change_request_comments = change_comments
            proposal.change_request_date = timezone.now()
            proposal.change_requested_by = request.user
            proposal.save()
            
            messages.success(request, 'Change request sent successfully! The school admin will be notified.')
            return redirect('grants:proposal_detail', proposal_id=proposal_id)
        
        return render(request, 'grants/proposal_request_changes.html', {'proposal': proposal})
    except Exception as e:
        import traceback
        print(f"Error in proposal_request_changes_view: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('grants:proposal_list')

@login_required
def proposal_resubmit_view(request, proposal_id):
    """Allow school admins to resubmit proposals after changes have been made."""
    try:
        proposal = get_object_or_404(GrantProposal, proposal_id=proposal_id)
        
        # Only allow resubmission for proposals that have changes requested
        if proposal.status != 'changes_requested':
            messages.warning(request, 'Only proposals with requested changes can be resubmitted.')
            return redirect('grants:proposal_detail', proposal_id=proposal_id)
        
        # Check if user is the creator of the proposal or has permission
        if not (request.user == proposal.created_by or request.user.is_system_admin()):
            messages.error(request, 'You do not have permission to resubmit this proposal.')
            return redirect('grants:proposal_detail', proposal_id=proposal_id)
        
        if request.method == 'POST':
            # Update proposal status to submitted
            proposal.status = 'submitted'
            proposal.submission_date = timezone.now()
            # Clear change request fields
            proposal.change_request_comments = ''
            proposal.change_request_date = None
            proposal.change_requested_by = None
            proposal.save()
            
            messages.success(request, 'Proposal resubmitted successfully! It will be reviewed again.')
            return redirect('grants:proposal_detail', proposal_id=proposal_id)
        
        return render(request, 'grants/proposal_resubmit.html', {'proposal': proposal})
    except Exception as e:
        import traceback
        print(f"Error in proposal_resubmit_view: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('grants:proposal_list') 