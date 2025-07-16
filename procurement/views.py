from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Tender, TenderDocument
from .forms import TenderForm, TenderDocumentForm, BidForm, BidWithCriteriaForm
from core.models import User
import pytesseract
from PIL import Image
import os
from PyPDF2 import PdfReader
from django.utils import timezone

from .models import Bid
from reporting.models import SupplierCriterionResponse
from ai_engine.ml_pipeline import predict, extract_features_from_ocr

# Create your views here.

def tender_list_view(request):
    tenders = Tender.objects.all().order_by('-created_at')
    return render(request, 'procurement/tender_list.html', {'tenders': tenders})

def get_bid_score(bid):
    features = {
        # Add static features as needed, e.g. proposal_text length
        'proposal_text_length': len(bid.proposal_text or ''),
    }
    # Add dynamic supplier criteria responses
    for response in bid.supplier.supplier_criterion_responses.all():
        if response.criterion.type == 'text':
            features[f'criterion_{response.criterion.id}_text'] = response.value_text or ''
        elif response.criterion.type == 'boolean':
            features[f'criterion_{response.criterion.id}_bool'] = int(response.value_bool) if response.value_bool is not None else 0
        elif response.criterion.type == 'file' and response.value_file:
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

def tender_detail_view(request, tender_id):
    tender = get_object_or_404(Tender, tender_id=tender_id)
    documents = tender.documents.all()
    bids = list(tender.bids.all())
    bid_scores = [(b, get_bid_score(b)) for b in bids]
    if bid_scores:
        min_score = min(s for _, s in bid_scores)
        max_score = max(s for _, s in bid_scores)
        if min_score == max_score:
            min_score = 0  # avoid division by zero
        for b, score in bid_scores:
            if max_score > min_score:
                norm_score = (score - min_score) / (max_score - min_score) * 99.9
                b.ml_score = '{:.1f}'.format(norm_score)
            else:
                b.ml_score = '99.9'
    else:
        for b, _ in bid_scores:
            b.ml_score = '0.0'
    bid_scores.sort(key=lambda x: float(x[0].ml_score), reverse=True)
    sorted_bids = [b for b, s in bid_scores]
    return render(request, 'procurement/tender_detail.html', {'tender': tender, 'documents': documents, 'bids': sorted_bids, 'bid_scores': dict(bid_scores)})

@login_required
@user_passes_test(lambda u: u.is_reb_officer() or u.is_system_admin())
def tender_create_view(request):
    if request.method == 'POST':
        form = TenderForm(request.POST)
        if form.is_valid():
            tender = form.save(commit=False)
            tender.created_by = request.user
            tender.save()
            messages.success(request, 'Tender created successfully!')
            return redirect('procurement:tender_detail', tender_id=tender.tender_id)
    else:
        form = TenderForm()
    return render(request, 'procurement/tender_form.html', {'form': form})

@login_required
def tender_document_upload_view(request, tender_id):
    tender = get_object_or_404(Tender, tender_id=tender_id)
    if request.method == 'POST':
        form = TenderDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.tender = tender
            doc.uploaded_by = request.user
            doc.file_size = doc.document_file.size
            # OCR logic
            uploaded_file = doc.document_file
            ocr_text = None
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
            doc.ocr_text = ocr_text
            doc.save()
            messages.success(request, 'Document uploaded successfully.' + (' OCR complete.' if ocr_text else ''))
            return redirect('procurement:tender_detail', tender_id=tender.tender_id)
    else:
        form = TenderDocumentForm()
    return render(request, 'procurement/tender_document_upload.html', {'form': form, 'tender': tender})

@login_required
@user_passes_test(lambda u: u.is_supplier())
def bid_submit_view(request, tender_id):
    tender = get_object_or_404(Tender, tender_id=tender_id)
    if request.method == 'POST':
        form = BidWithCriteriaForm(request.POST, request.FILES)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.tender = tender
            bid.supplier = request.user
            bid.save()
            # Save criterion responses
            for field_name, field in form.fields.items():
                if hasattr(field, 'criterion_obj'):
                    criterion = field.criterion_obj
                    value = form.cleaned_data.get(field_name)
                    response_kwargs = {'supplier': request.user, 'criterion': criterion}
                    if criterion.type == 'file':
                        SupplierCriterionResponse.objects.update_or_create(
                            **response_kwargs,
                            defaults={'value_file': value, 'value_text': None, 'value_bool': None}
                        )
                    elif criterion.type == 'text':
                        SupplierCriterionResponse.objects.update_or_create(
                            **response_kwargs,
                            defaults={'value_text': value, 'value_file': None, 'value_bool': None}
                        )
                    elif criterion.type == 'boolean':
                        SupplierCriterionResponse.objects.update_or_create(
                            **response_kwargs,
                            defaults={'value_bool': value, 'value_file': None, 'value_text': None}
                        )
            messages.success(request, 'Your bid has been submitted!')
            return redirect('procurement:tender_detail', tender_id=tender.tender_id)
    else:
        form = BidWithCriteriaForm()
    return render(request, 'procurement/bid_submit.html', {'form': form, 'tender': tender})

@login_required
@user_passes_test(lambda u: u.is_reb_officer() or u.is_system_admin())
def award_bid_view(request, tender_id, bid_id):
    tender = get_object_or_404(Tender, tender_id=tender_id)
    bid = get_object_or_404(Bid, bid_id=bid_id, tender=tender)
    if request.method == 'POST':
        # Set all other bids to rejected
        tender.bids.exclude(pk=bid.pk).update(status='rejected')
        # Award this bid
        bid.status = 'awarded'
        bid.awarded_at = timezone.now()
        bid.save()
        # Update tender
        tender.status = 'awarded'
        tender.awarded_to = bid.supplier.get_full_name() or bid.supplier.username
        tender.save()
        messages.success(request, f'Bid by {tender.awarded_to} has been awarded.')
    return redirect('procurement:tender_detail', tender_id=tender.tender_id)
