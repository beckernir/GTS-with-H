from django.core.management.base import BaseCommand
from grants.models import GrantProposal

class Command(BaseCommand):
    help = 'Print all GrantProposal records with their id, created_at values, and type of created_at.'

    def handle(self, *args, **options):
        for p in GrantProposal.objects.all():
            self.stdout.write(f'ID: {p.id}, created_at: {p.created_at}, type: {type(p.created_at)}') 