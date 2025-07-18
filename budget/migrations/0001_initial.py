# Generated by Django 4.2.23 on 2025-06-29 17:59

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BudgetCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('category_name', models.CharField(max_length=100)),
                ('category_type', models.CharField(choices=[('personnel', 'Personnel Costs'), ('equipment', 'Equipment and Materials'), ('infrastructure', 'Infrastructure'), ('services', 'Services and Contracts'), ('travel', 'Travel and Transportation'), ('utilities', 'Utilities and Maintenance'), ('training', 'Training and Development'), ('supplies', 'Supplies and Consumables'), ('technology', 'Technology and ICT'), ('other', 'Other Costs')], default='other', max_length=20)),
                ('description', models.TextField(blank=True, null=True)),
                ('budget_limit', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('allocated_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('spent_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('is_active', models.BooleanField(default=True)),
                ('requires_approval', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Budget Category',
                'verbose_name_plural': 'Budget Categories',
                'db_table': 'budget_budget_category',
                'ordering': ['category_type', 'category_name'],
            },
        ),
        migrations.CreateModel(
            name='BudgetLineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_item_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('item_description', models.CharField(max_length=200)),
                ('item_details', models.TextField(blank=True, null=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('unit_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=12)),
                ('allocated_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('spent_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('committed_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('status', models.CharField(choices=[('planned', 'Planned'), ('approved', 'Approved'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='planned', max_length=20)),
                ('planned_date', models.DateField()),
                ('completion_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Budget Line Item',
                'verbose_name_plural': 'Budget Line Items',
                'db_table': 'budget_budget_line_item',
                'ordering': ['budget_category', 'item_description'],
            },
        ),
        migrations.CreateModel(
            name='BudgetPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('period_name', models.CharField(max_length=100, unique=True)),
                ('period_type', models.CharField(choices=[('fiscal_year', 'Fiscal Year'), ('quarter', 'Quarter'), ('semester', 'Semester'), ('monthly', 'Monthly'), ('custom', 'Custom Period')], default='fiscal_year', max_length=20)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('total_budget_limit', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('allocated_budget', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('spent_budget', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('is_active', models.BooleanField(default=True)),
                ('is_closed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Budget Period',
                'verbose_name_plural': 'Budget Periods',
                'db_table': 'budget_budget_period',
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='BudgetReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('report_type', models.CharField(choices=[('monthly', 'Monthly Report'), ('quarterly', 'Quarterly Report'), ('annual', 'Annual Report'), ('variance', 'Variance Analysis'), ('forecast', 'Budget Forecast'), ('custom', 'Custom Report')], default='monthly', max_length=20)),
                ('report_title', models.CharField(max_length=200)),
                ('report_period_start', models.DateField()),
                ('report_period_end', models.DateField()),
                ('report_data', models.JSONField(default=dict, help_text='JSON object containing report data')),
                ('summary', models.TextField(blank=True, null=True)),
                ('report_file', models.FileField(blank=True, null=True, upload_to='budget_reports/')),
                ('generated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Budget Report',
                'verbose_name_plural': 'Budget Reports',
                'db_table': 'budget_budget_report',
                'ordering': ['-generated_at'],
            },
        ),
        migrations.CreateModel(
            name='BudgetTransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transfer_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('transfer_type', models.CharField(choices=[('within_category', 'Within Category'), ('between_categories', 'Between Categories'), ('between_budgets', 'Between Budgets'), ('adjustment', 'Budget Adjustment')], default='within_category', max_length=20)),
                ('transfer_amount', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('transfer_date', models.DateField()),
                ('reason', models.TextField()),
                ('is_approved', models.BooleanField(default=False)),
                ('approval_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Budget Transfer',
                'verbose_name_plural': 'Budget Transfers',
                'db_table': 'budget_budget_transfer',
                'ordering': ['-transfer_date'],
            },
        ),
        migrations.CreateModel(
            name='Expenditure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expenditure_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('expenditure_type', models.CharField(choices=[('actual', 'Actual Expenditure'), ('commitment', 'Commitment'), ('adjustment', 'Budget Adjustment'), ('transfer', 'Budget Transfer')], default='actual', max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('description', models.CharField(max_length=200)),
                ('details', models.TextField(blank=True, null=True)),
                ('payment_method', models.CharField(choices=[('cash', 'Cash'), ('bank_transfer', 'Bank Transfer'), ('check', 'Check'), ('mobile_money', 'Mobile Money'), ('other', 'Other')], default='bank_transfer', max_length=20)),
                ('payment_reference', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_date', models.DateField()),
                ('supplier_name', models.CharField(blank=True, max_length=200, null=True)),
                ('supplier_contact', models.CharField(blank=True, max_length=100, null=True)),
                ('receipt_number', models.CharField(blank=True, max_length=50, null=True)),
                ('invoice_number', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Expenditure',
                'verbose_name_plural': 'Expenditures',
                'db_table': 'budget_expenditure',
                'ordering': ['-payment_date'],
            },
        ),
        migrations.CreateModel(
            name='SchoolBudget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('budget_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('budget_title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved'), ('active', 'Active'), ('closed', 'Closed'), ('cancelled', 'Cancelled')], default='draft', max_length=20)),
                ('total_budget_amount', models.DecimalField(decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('allocated_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('spent_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('committed_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('submission_date', models.DateTimeField(blank=True, null=True)),
                ('approval_date', models.DateTimeField(blank=True, null=True)),
                ('activation_date', models.DateTimeField(blank=True, null=True)),
                ('closure_date', models.DateTimeField(blank=True, null=True)),
                ('approval_notes', models.TextField(blank=True, null=True)),
                ('rejection_reason', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'School Budget',
                'verbose_name_plural': 'School Budgets',
                'db_table': 'budget_school_budget',
                'ordering': ['-created_at'],
            },
        ),
    ]
