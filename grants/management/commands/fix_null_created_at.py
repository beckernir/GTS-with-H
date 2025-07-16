from django.core.management.base import BaseCommand
from grants.models import GrantProposal
from django.utils import timezone

class Command(BaseCommand):
    help = 'Fix GrantProposal records with null created_at by setting to submission_date, approval_date, or now.'

    def handle(self, *args, **options):
        qs = GrantProposal.objects.filter(created_at__isnull=True)
        count = qs.count()
        self.stdout.write(f'Found {count} proposals with null created_at.')
        fixed = 0
        for p in qs:
            p.created_at = p.submission_date or p.approval_date or timezone.now()
            p.save()
            fixed += 1
            self.stdout.write(f'Fixed proposal {p.id}')
        self.stdout.write(self.style.SUCCESS(f'Fixed {fixed} proposals.')) 