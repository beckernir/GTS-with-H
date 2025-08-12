# Generated manually to add current_amount field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0002_proposaldocument_ocr_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='grantproposal',
            name='current_amount',
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                help_text='Current available budget for this project',
                max_digits=12
            ),
        ),
    ] 