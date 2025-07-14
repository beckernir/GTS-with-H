from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import School
from budget.models import BudgetPeriod, SchoolBudget, BudgetCategory, BudgetLineItem, BudgetTransfer
from django.utils import timezone
import datetime

class Command(BaseCommand):
    help = 'Add dummy data for testing budget transfers.'

    def handle(self, *args, **options):
        User = get_user_model()
        user, _ = User.objects.get_or_create(username='admin', defaults={'is_staff': True, 'is_superuser': True})
        school, _ = School.objects.get_or_create(school_name='Test School', defaults={'status': 'active'})
        period, _ = BudgetPeriod.objects.get_or_create(period_name='2024-2025', defaults={
            'period_type': 'fiscal_year',
            'start_date': datetime.date(2024, 7, 1),
            'end_date': datetime.date(2025, 6, 30),
            'total_budget_limit': 10000000,
            'allocated_budget': 8000000,
            'spent_budget': 2000000,
            'is_active': True,
            'is_closed': False,
            'created_by': user,
        })
        category, _ = BudgetCategory.objects.get_or_create(category_name='Instructional Materials', defaults={
            'category_type': 'equipment',
            'budget_limit': 2000000,
            'allocated_amount': 1500000,
            'spent_amount': 500000,
            'is_active': True,
            'requires_approval': False,
        })
        budget, _ = SchoolBudget.objects.get_or_create(school=school, budget_period=period, defaults={
            'budget_title': 'Test Budget',
            'description': 'Dummy budget for testing transfers',
            'status': 'active',
            'total_budget_amount': 1500000,
            'allocated_amount': 1500000,
            'spent_amount': 500000,
            'committed_amount': 0,
            'created_by': user,
        })
        line_item1, _ = BudgetLineItem.objects.get_or_create(school_budget=budget, budget_category=category, item_description='Books', defaults={
            'quantity': 100,
            'unit_cost': 10000,
            'allocated_amount': 1000000,
            'spent_amount': 200000,
            'committed_amount': 0,
            'status': 'planned',
            'planned_date': timezone.now().date(),
            'created_by': user,
        })
        line_item2, _ = BudgetLineItem.objects.get_or_create(school_budget=budget, budget_category=category, item_description='Notebooks', defaults={
            'quantity': 200,
            'unit_cost': 5000,
            'allocated_amount': 500000,
            'spent_amount': 300000,
            'committed_amount': 0,
            'status': 'planned',
            'planned_date': timezone.now().date(),
            'created_by': user,
        })
        transfer, _ = BudgetTransfer.objects.get_or_create(
            source_line_item=line_item1,
            destination_line_item=line_item2,
            transfer_amount=100000,
            transfer_date=timezone.now().date(),
            defaults={
                'transfer_type': 'within_category',
                'reason': 'Reallocate funds for more notebooks',
                'created_by': user,
                'is_approved': True,
                'approval_date': timezone.now(),
            }
        )
        self.stdout.write(self.style.SUCCESS('Dummy data for budget transfer created.')) 