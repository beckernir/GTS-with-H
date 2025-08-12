from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('budget', '0002_initial'),
    ]
    operations = [
        migrations.AddField(
            model_name='schoolbudget',
            name='requesting_amount',
            field=models.DecimalField(max_digits=15, decimal_places=2, default=0.00, help_text='Amount being requested for this budget.'),
        ),
    ]