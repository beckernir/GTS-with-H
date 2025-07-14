from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from grants.models import GrantProposal
from core.models import School
from budget.models import SchoolBudget
import csv
import os

def export_training_data():
    from grants.models import GrantProposal
    from core.models import School
    from budget.models import SchoolBudget
    out_dir = 'ai_engine/dataset'
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'training_data.csv')
    fieldnames = [
        'proposal_id', 'proposal_title', 'school', 'district', 'grant_category', 'requested_amount',
        'status', 'created_at', 'approval_date', 'start_date', 'end_date', 'description',
        'school_id', 'school_name', 'school_district', 'school_level', 'school_status',
        'budget_id', 'budget_title', 'budget_amount', 'budget_status'
    ]
    schools = {s.id: s for s in School.objects.all()}
    budgets = {b.id: b for b in SchoolBudget.objects.all()}
    with open(out_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for p in GrantProposal.objects.all():
            school = schools.get(p.school_id) if p.school_id else None
            budget = None
            # Try to find a budget for the school
            if school:
                for b in budgets.values():
                    if b.school_id == school.id:
                        budget = b
                        break
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
                'school_id': school.id if school else '',
                'school_name': school.school_name if school else '',
                'school_district': school.district if school else '',
                'school_level': school.level if school else '',
                'school_status': school.status if school else '',
                'budget_id': budget.id if budget else '',
                'budget_title': budget.budget_title if budget else '',
                'budget_amount': budget.total_budget_amount if budget else '',
                'budget_status': budget.status if budget else '',
            })

@receiver(post_save, sender=GrantProposal)
def update_training_data_csv_on_save(sender, instance, **kwargs):
    export_training_data()

@receiver(post_delete, sender=GrantProposal)
def update_training_data_csv_on_delete(sender, instance, **kwargs):
    export_training_data()

@receiver(post_save, sender=School)
def update_training_data_csv_on_school_save(sender, instance, **kwargs):
    export_training_data()

@receiver(post_delete, sender=School)
def update_training_data_csv_on_school_delete(sender, instance, **kwargs):
    export_training_data()

@receiver(post_save, sender=SchoolBudget)
def update_training_data_csv_on_budget_save(sender, instance, **kwargs):
    export_training_data()

@receiver(post_delete, sender=SchoolBudget)
def update_training_data_csv_on_budget_delete(sender, instance, **kwargs):
    export_training_data() 