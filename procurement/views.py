from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Tender, TenderDocument
from .forms import TenderForm, TenderDocumentForm, BidForm
from core.models import User
import pytesseract
from PIL import Image
import os
from PyPDF2 import PdfReader
from django.utils import timezone

from .models import Bid

# Create your views here.

def tender_list_view(request):
    tenders = Tender.objects.all().order_by('-created_at')
    return render(request, 'procurement/tender_list.html', {'tenders': tenders})

def tender_detail_view(request, tender_id):
    tender = get_object_or_404(Tender, tender_id=tender_id)
    documents = tender.documents.all()
    bids = tender.bids.all().order_by('-submitted_at')
    return render(request, 'procurement/tender_detail.html', {'tender': tender, 'documents': documents, 'bids': bids})

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
        form = BidForm(request.POST, request.FILES)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.tender = tender
            bid.supplier = request.user
            bid.save()
            messages.success(request, 'Your bid has been submitted!')
            return redirect('procurement:tender_detail', tender_id=tender.tender_id)
    else:
        form = BidForm()
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
