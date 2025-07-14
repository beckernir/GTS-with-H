from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Tender, TenderDocument
from .forms import TenderForm, TenderDocumentForm
from core.models import User
import pytesseract
from PIL import Image
import os
from PyPDF2 import PdfReader

# Create your views here.

def tender_list_view(request):
    tenders = Tender.objects.all().order_by('-created_at')
    return render(request, 'procurement/tender_list.html', {'tenders': tenders})

def tender_detail_view(request, tender_id):
    tender = get_object_or_404(Tender, tender_id=tender_id)
    documents = tender.documents.all()
    return render(request, 'procurement/tender_detail.html', {'tender': tender, 'documents': documents})

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
