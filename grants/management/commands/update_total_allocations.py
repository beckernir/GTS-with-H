from django.core.management.base import BaseCommand
from grants.models import GrantProposal, TotalGrantAllocation
from django.db.models import Sum
from decimal import Decimal


class Command(BaseCommand):
    help = 'Update TotalGrantAllocation records with actual funded amounts from GrantProposal data'

    def handle(self, *args, **options):
        # Get all total allocations
        total_allocations = TotalGrantAllocation.objects.all()
        
        for allocation in total_allocations:
            # Get all funded and approved proposals for this fiscal year
            proposals_in_year = GrantProposal.objects.filter(
                created_at__year=allocation.fiscal_year
            )
            
            # Calculate actual allocated amount (sum of current_amount for funded/approved proposals)
            actual_allocated = proposals_in_year.filter(
                status__in=['funded', 'approved']
            ).aggregate(
                total=Sum('current_amount')
            )['total'] or Decimal('0.00')
            
            # Calculate actual disbursed amount (sum of disbursed_amount for funded/approved proposals)
            actual_disbursed = proposals_in_year.filter(
                status__in=['funded', 'approved']
            ).aggregate(
                total=Sum('disbursed_amount')
            )['total'] or Decimal('0.00')
            
            # Update the allocation record
            old_allocated = allocation.allocated_amount
            old_disbursed = allocation.disbursed_amount
            
            allocation.allocated_amount = actual_allocated
            allocation.disbursed_amount = actual_disbursed
            allocation.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'FY {allocation.fiscal_year}: '
                    f'Allocated: {old_allocated} -> {actual_allocated}, '
                    f'Disbursed: {old_disbursed} -> {actual_disbursed}'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {total_allocations.count()} total allocation records'
            )
        )
