from django.core.management.base import BaseCommand
from ai_engine.ml_pipeline import train_model

class Command(BaseCommand):
    help = 'Train the ML model on the current training data.'
 
    def handle(self, *args, **options):
        acc = train_model()
        self.stdout.write(self.style.SUCCESS(f'Model trained. Accuracy: {acc:.2%}')) 