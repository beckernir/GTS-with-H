# Generated by Django 4.2.23 on 2025-07-16 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0002_rebgrantbudget'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProposalCriterion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('type', models.CharField(choices=[('file', 'File Upload'), ('text', 'Text'), ('boolean', 'Yes/No')], default='file', max_length=10)),
                ('required', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True)),
                ('ordering', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Proposal Criterion',
                'verbose_name_plural': 'Proposal Criteria',
                'db_table': 'reporting_proposal_criterion',
                'ordering': ['ordering', 'name'],
            },
        ),
        migrations.CreateModel(
            name='SupplierCriterion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('type', models.CharField(choices=[('file', 'File Upload'), ('text', 'Text'), ('boolean', 'Yes/No')], default='file', max_length=10)),
                ('required', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True)),
                ('ordering', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Supplier Criterion',
                'verbose_name_plural': 'Supplier Criteria',
                'db_table': 'reporting_supplier_criterion',
                'ordering': ['ordering', 'name'],
            },
        ),
    ]
