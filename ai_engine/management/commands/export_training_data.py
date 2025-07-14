import csv
from django.core.management.base import BaseCommand
from grants.models import GrantProposal
from core.models import School
from grants.models import GrantCategory
from django.utils import timezone
import os

class Command(BaseCommand):
    help = 'Export GrantProposal data as a CSV for ML training.'

    def handle(self, *args, **options):
        out_dir = 'ai_engine/dataset'
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, 'training_data.csv')
        fieldnames = [
            'proposal_id', 'proposal_title', 'school', 'district', 'grant_category', 'requested_amount',
            'status', 'created_at', 'approval_date', 'start_date', 'end_date', 'description'
        ]
        with open(out_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for p in GrantProposal.objects.all():
                writer.writerow({
                    'proposal_id': str(p.proposal_id) if hasattr(p, 'proposal_id') else p.id,
                    'proposal_title': p.proposal_title,
                    'school': p.school.school_name if p.school else '',
                    'district': p.school.district if p.school else '',
                    'grant_category': p.grant_category.category_name if p.grant_category else '',
                    'requested_amount': p.requested_amount,
                    'status': p.status,
                    'created_at': p.created_at.strftime('%Y-%m-%d') if p.created_at else '',
                    'approval_date': p.approval_date.strftime('%Y-%m-%d') if hasattr(p, 'approval_date') and p.approval_date else '',
                    'start_date': p.start_date.strftime('%Y-%m-%d') if hasattr(p, 'start_date') and p.start_date else '',
                    'end_date': p.end_date.strftime('%Y-%m-%d') if hasattr(p, 'end_date') and p.end_date else '',
                    'description': p.description or '',
                })
        self.stdout.write(self.style.SUCCESS(f'Training data exported to {out_path}')) 