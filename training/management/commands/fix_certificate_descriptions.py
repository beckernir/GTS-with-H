from django.core.management.base import BaseCommand
from training.models import TrainingCertificate
from django.template import Template, Context


class Command(BaseCommand):
    help = 'Fix certificate descriptions that contain template variables instead of actual values'

    def handle(self, *args, **options):
        certificates = TrainingCertificate.objects.all()
        fixed_count = 0
        
        for certificate in certificates:
            description = certificate.description
            
            # Check if description contains template variables
            if '{{' in description and '}}' in description:
                self.stdout.write(f"Fixing certificate {certificate.certificate_id}: {description[:100]}...")
                
                try:
                    # Create a template context with the certificate data
                    context = Context({
                        'certificate': certificate,
                        'ach': certificate.achievements[0] if certificate.achievements else {}
                    })
                    
                    # Process the template
                    template = Template(description)
                    processed_description = template.render(context)
                    
                    # Update the certificate
                    certificate.description = processed_description
                    certificate.save(update_fields=['description'])
                    
                    fixed_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Fixed: {processed_description[:100]}..."))
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing certificate {certificate.certificate_id}: {e}"))
                    
                    # Fallback: generate a proper description
                    recipient = certificate.enrollment.user.get_full_name() or certificate.enrollment.user.username
                    course_title = certificate.enrollment.course.course_title
                    
                    # Try to get score from achievements
                    score = "100.0"
                    if certificate.achievements:
                        for ach in certificate.achievements:
                            if isinstance(ach, dict) and ach.get('label') == 'Score':
                                score = ach.get('value', '100.0')
                                break
                    
                    fallback_description = f"Awarded to {recipient} for successfully completing the course with a score of {score}%."
                    certificate.description = fallback_description
                    certificate.save(update_fields=['description'])
                    
                    fixed_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Fixed with fallback: {fallback_description}"))
        
        self.stdout.write(self.style.SUCCESS(f"Successfully fixed {fixed_count} certificates"))
