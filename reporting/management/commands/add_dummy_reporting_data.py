from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import User, School
from reporting.models import Report, KPI, KPIValue, AnalyticsEvent, DataExport
from budget.models import SchoolBudget, BudgetPeriod, BudgetReport
import random
import uuid
from datetime import timedelta
from grants.models import GrantProposal, GrantCategory

class Command(BaseCommand):
    help = 'Populate the database with dummy data for all reporting and related models.'

    def handle(self, *args, **options):
        # 1. Users
        roles = ['reb_officer', 'school_admin', 'teacher', 'system_admin']
        users = []
        for i, role in enumerate(roles):
            user, _ = User.objects.get_or_create(
                username=f'dummy_{role}',
                defaults={
                    'email': f'{role}@example.com',
                    'role': role,
                    'status': 'active',
                    'first_name': role.capitalize(),
                    'last_name': 'User',
                    'is_active': True,
                }
            )
            users.append(user)
        # 2. School
        school, _ = School.objects.get_or_create(
            school_code='SCH001',
            defaults={
                'school_name': 'Dummy Secondary School',
                'district': 'Kigali',
                'sector': 'Gasabo',
                'cell': 'Kacyiru',
                'village': 'Village A',
                'address': '123 Main St',
                'created_by': users[0],
            }
        )
        # 2b. Add dummy GrantProposals in various districts
        districts = ['Kigali', 'Eastern', 'Western', 'Southern', 'Northern']
        category, _ = GrantCategory.objects.get_or_create(category_name='Education', defaults={'description': 'Education grants'})
        for i, district in enumerate(districts):
            school_obj, _ = School.objects.get_or_create(
                school_code=f'SCH00{i+2}',
                defaults={
                    'school_name': f'Dummy School {district}',
                    'district': district,
                    'sector': 'Sector X',
                    'cell': 'Cell Y',
                    'village': 'Village Z',
                    'address': f'{district} Main St',
                    'created_by': users[0],
                }
            )
            for j in range(3):
                GrantProposal.objects.get_or_create(
                    proposal_title=f'Grant Proposal {district} {j+1}',
                    school=school_obj,
                    grant_category=category,
                    defaults={
                        'requested_amount': 1000000 * (i+1) * (j+1),
                        'status': 'approved',
                        'created_by': users[0],
                        'created_at': timezone.now() - timedelta(days=30*(j+1)),
                        'approval_date': timezone.now() - timedelta(days=30*j),
                        'description': f'Dummy proposal for {district}',
                        'start_date': timezone.now().date() - timedelta(days=60),
                        'end_date': timezone.now().date() + timedelta(days=60),
                    }
                )
        # 3. BudgetPeriod and SchoolBudget
        period, _ = BudgetPeriod.objects.get_or_create(
            period_name='2024 Fiscal Year',
            defaults={
                'period_type': 'fiscal_year',
                'start_date': timezone.now().date() - timedelta(days=180),
                'end_date': timezone.now().date() + timedelta(days=180),
                'created_by': users[0],
            }
        )
        school_budget, _ = SchoolBudget.objects.get_or_create(
            school=school,
            budget_period=period,
            defaults={
                'budget_title': '2024 Main Budget',
                'description': 'Main budget for 2024',
                'status': 'approved',
                'total_budget_amount': 10000000,
                'created_by': users[0],
            }
        )
        # 4. KPIs
        kpi_objs = []
        for i in range(5):
            kpi, _ = KPI.objects.get_or_create(
                kpi_name=f'Dummy KPI {i+1}',
                defaults={
                    'kpi_category': random.choice(['financial', 'operational', 'academic']),
                    'kpi_type': random.choice(['count', 'percentage', 'currency']),
                    'description': f'Description for KPI {i+1}',
                    'calculation_formula': 'Random formula',
                    'unit_of_measure': 'units',
                    'target_value': 100,
                    'threshold_value': 80,
                    'min_value': 0,
                    'max_value': 200,
                    'is_active': True,
                    'is_system': False,
                    'auto_calculate': True,
                    'applicable_roles': ['reb_officer', 'school_admin'],
                    'created_by': users[0],
                }
            )
            kpi_objs.append(kpi)
        # 5. KPIValues
        for kpi in kpi_objs:
            for j in range(6):
                KPIValue.objects.get_or_create(
                    kpi=kpi,
                    measurement_date=timezone.now().date() - timedelta(days=30*j),
                    measurement_period='Monthly',
                    defaults={
                        'value': random.uniform(50, 150),
                        'school': school,
                        'context_data': {},
                        'is_above_target': random.choice([True, False]),
                        'is_above_threshold': random.choice([True, False]),
                        'performance_status': random.choice(['excellent', 'good', 'fair', 'poor', 'critical']),
                        'calculated_by': users[0],
                    }
                )
        # 6. Reports (all types)
        report_types = [c[0] for c in Report.REPORT_TYPE_CHOICES]
        for rtype in report_types:
            for i in range(3):
                Report.objects.get_or_create(
                    report_name=f'{rtype.replace("_", " ").title()} {i+1}',
                    report_type=rtype,
                    format='pdf',
                    created_by=users[0],
                    defaults={
                        'description': f'Dummy {rtype} report',
                        'parameters': {},
                        'school': school,
                        'status': 'completed',
                        'row_count': random.randint(10, 100),
                        'generation_time_seconds': random.randint(1, 10),
                        'created_at': timezone.now() - timedelta(days=random.randint(1, 60)),
                    }
                )
        # 7. BudgetReport
        for i in range(3):
            BudgetReport.objects.get_or_create(
                report_title=f'Monthly Budget Report {i+1}',
                report_type='monthly',
                school_budget=school_budget,
                report_period_start=timezone.now().date() - timedelta(days=30*(i+1)),
                report_period_end=timezone.now().date() - timedelta(days=30*i),
                defaults={
                    'report_data': {'amount': random.randint(100000, 500000)},
                    'summary': 'Dummy summary',
                    'generated_by': users[0],
                }
            )
        # 8. AnalyticsEvent
        for i in range(10):
            AnalyticsEvent.objects.get_or_create(
                event_name=f'Dummy Event {i+1}',
                event_type=random.choice(['page_view', 'button_click', 'report_generate']),
                user=users[0],
                defaults={
                    'event_data': {},
                    'metadata': {},
                    'timestamp': timezone.now() - timedelta(days=random.randint(1, 30)),
                }
            )
        # 9. DataExport
        for i in range(5):
            DataExport.objects.get_or_create(
                export_type=random.choice(['grants', 'budgets', 'reports', 'users', 'schools']),
                format=random.choice(['csv', 'excel', 'pdf']),
                user=users[0],
                defaults={
                    'description': 'Dummy export',
                    'filters': {},
                    'status': 'completed',
                    'row_count': random.randint(10, 100),
                    'processing_time_seconds': random.randint(1, 10),
                    'download_count': random.randint(1, 10),
                    'created_at': timezone.now() - timedelta(days=random.randint(1, 30)),
                }
            )
        self.stdout.write(self.style.SUCCESS('Dummy data created for all reporting and related models!')) 