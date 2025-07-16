from django.core.management.base import BaseCommand
from reporting.models import ProposalCriterion, SupplierCriterion

class Command(BaseCommand):
    help = 'Load demo criteria for proposals and suppliers.'

    def handle(self, *args, **options):
        # Proposal Criteria
        proposal_criteria = [
            dict(name='Financial transparency & Reporting', description='Upload file for financial transparency and reporting.', type='file', required=True, ordering=1),
            dict(name='Performance Monitoring & Evaluation', description='Upload file for performance monitoring and evaluation.', type='file', required=True, ordering=2),
            dict(name='Legal registration', description='Official legal registration document.', type='file', required=True, ordering=3),
            dict(name='Insurance', description='Proof of insurance.', type='file', required=False, ordering=4),
        ]
        for c in proposal_criteria:
            ProposalCriterion.objects.update_or_create(name=c['name'], defaults=c)
        self.stdout.write(self.style.SUCCESS('Loaded proposal criteria.'))

        # Supplier Criteria
        supplier_criteria = [
            dict(name='Legal Registration (TIN)', description='TIN certificate for legal registration.', type='file', required=True, ordering=1),
            dict(name='Quality assurance', description='Quality assurance documentation.', type='file', required=True, ordering=2),
            dict(name='RPPA certificate', description='Upload RPPA certificate.', type='file', required=True, ordering=3),
            dict(name='Contract proposal', description='Upload contract proposal.', type='file', required=True, ordering=4),
            dict(name='Payment terms', description='Specify payment terms.', type='text', required=True, ordering=5),
        ]
        for c in supplier_criteria:
            SupplierCriterion.objects.update_or_create(name=c['name'], defaults=c)
        self.stdout.write(self.style.SUCCESS('Loaded supplier criteria.')) 