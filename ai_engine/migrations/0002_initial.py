# Generated by Django 4.2.23 on 2025-06-29 17:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
        ('grants', '0001_initial'),
        ('ai_engine', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='riskassessment',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_risk_assessments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='riskassessment',
            name='proposal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='risk_assessments', to='grants.grantproposal'),
        ),
        migrations.AddField(
            model_name='riskassessment',
            name='resolved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resolved_risk_assessments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='riskassessment',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='risk_assessments', to='core.school'),
        ),
        migrations.AddField(
            model_name='proposalallocationscore',
            name='allocation_run',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposal_scores', to='ai_engine.allocationrun'),
        ),
        migrations.AddField(
            model_name='proposalallocationscore',
            name='proposal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocation_scores', to='grants.grantproposal'),
        ),
        migrations.AddField(
            model_name='optimizationrecommendation',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_recommendations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='optimizationrecommendation',
            name='implemented_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='implemented_recommendations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='optimizationrecommendation',
            name='proposal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='optimization_recommendations', to='grants.grantproposal'),
        ),
        migrations.AddField(
            model_name='optimizationrecommendation',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='optimization_recommendations', to='core.school'),
        ),
        migrations.AddField(
            model_name='allocationrun',
            name='algorithm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocation_runs', to='ai_engine.allocationalgorithm'),
        ),
        migrations.AddField(
            model_name='allocationrun',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='initiated_allocation_runs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='allocationfactor',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_factors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='allocationalgorithm',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_algorithms', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='proposalallocationscore',
            unique_together={('allocation_run', 'proposal')},
        ),
    ]
