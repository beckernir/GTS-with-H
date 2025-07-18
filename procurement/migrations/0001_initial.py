# Generated by Django 4.2.23 on 2025-07-14 04:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_auditlog'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tender_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('open', 'Open for Submission'), ('closed', 'Closed'), ('awarded', 'Awarded'), ('cancelled', 'Cancelled')], default='draft', max_length=20)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('submission_deadline', models.DateTimeField()),
                ('awarded_to', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_tenders', to=settings.AUTH_USER_MODEL)),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tenders', to='core.school')),
            ],
        ),
        migrations.CreateModel(
            name='TenderStatusHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_status', models.CharField(max_length=20)),
                ('new_status', models.CharField(max_length=20)),
                ('changed_at', models.DateTimeField(auto_now_add=True)),
                ('changed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tender_status_changes', to=settings.AUTH_USER_MODEL)),
                ('tender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_history', to='procurement.tender')),
            ],
        ),
        migrations.CreateModel(
            name='TenderDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('document_type', models.CharField(choices=[('specification', 'Specification'), ('bid', 'Bid Submission'), ('award', 'Award Letter'), ('other', 'Other')], default='other', max_length=20)),
                ('document_title', models.CharField(max_length=200)),
                ('document_file', models.FileField(upload_to='tender_documents/')),
                ('file_size', models.PositiveIntegerField(help_text='File size in bytes')),
                ('description', models.TextField(blank=True, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('ocr_text', models.TextField(blank=True, help_text='Extracted text from OCR analysis.', null=True)),
                ('tender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='procurement.tender')),
                ('uploaded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uploaded_tender_documents', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
