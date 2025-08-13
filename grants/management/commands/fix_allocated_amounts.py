from django.core.management.base import BaseCommand
from grants.models import GrantProposal


class Command(BaseCommand):
    help = 'Fix allocated amounts for approved and funded proposals that have 0 allocated amounts'

    def handle(self, *args, **options):
        # Get all approved and funded proposals with 0 allocated amounts
        proposals_to_fix = GrantProposal.objects.filter(
            status__in=['approved', 'funded'],
            allocated_amount=0
        )
        
        count = 0
        for proposal in proposals_to_fix:
            # Set allocated amount to requested amount
            proposal.allocated_amount = proposal.requested_amount
            proposal.current_amount = proposal.requested_amount
            proposal.save()
            count += 1
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Fixed proposal {proposal.proposal_code}: '
                    f'{proposal.requested_amount} -> {proposal.allocated_amount}'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully fixed {count} proposals with allocated amounts'
            )
        )
