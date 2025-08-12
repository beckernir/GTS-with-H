from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('budget', '0003_add_requesting_amount'),
    ]
    operations = [
        migrations.CreateModel(
            name='BudgetDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criteria', models.CharField(max_length=20, choices=[
                    ('plan', 'Budget Plan'),
                    ('approval', 'Approval Letter'),
                    ('report', 'Previous Report'),
                    ('quote', 'Supplier Quote'),
                    ('other', 'Other Required Doc'),
                ])),
                ('document', models.FileField(upload_to='budget_documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('school_budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='budget.schoolbudget')),
            ],
            options={
                'unique_together': {('school_budget', 'criteria')},
                'verbose_name': 'Budget Document',
                'verbose_name_plural': 'Budget Documents',
            },
        ),
    ]