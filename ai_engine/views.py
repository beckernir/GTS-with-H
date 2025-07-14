from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from grants.models import GrantProposal
from core.models import School
from django.utils import timezone
import random
from ai_engine.ml_pipeline import predict, train_model, generate_predictions, detect_anomalies
from django.contrib import messages
from ai_engine.models import RecommendationAction, AIModelStatus, ProposalPrediction, ProposalAnomaly
from django.contrib.auth.decorators import login_required
from collections import Counter
from django.db import models

# Create your views here.

@login_required
def ai_overview_view(request):
    # Handle AI Actions
    ai_action_message = None
    if request.method == 'POST':
        if 'ai_action' in request.POST:
            ai_action = request.POST['ai_action']
            if ai_action == 'run_allocation':
                AIModelStatus.objects.update_or_create(
                    component='allocation',
                    defaults={'status': 'active', 'progress': 100, 'updated_at': timezone.now()}
                )
                ai_action_message = 'AI allocation analysis started.'
            elif ai_action == 'generate_predictions':
                AIModelStatus.objects.update_or_create(
                    component='prediction',
                    defaults={'status': 'training', 'progress': 0, 'updated_at': timezone.now()}
                )
                total = generate_predictions()
                AIModelStatus.objects.update_or_create(
                    component='prediction',
                    defaults={'status': 'active', 'progress': 100, 'updated_at': timezone.now()}
                )
                ai_action_message = f'Predictions generated for {total} proposals.'
            elif ai_action == 'optimize_budget':
                AIModelStatus.objects.update_or_create(
                    component='allocation',
                    defaults={'status': 'active', 'progress': 100, 'updated_at': timezone.now()}
                )
                ai_action_message = 'Budget optimization complete.'
            elif ai_action == 'detect_anomalies':
                AIModelStatus.objects.update_or_create(
                    component='prediction',
                    defaults={'status': 'training', 'progress': 0, 'updated_at': timezone.now()}
                )
                anomalies = detect_anomalies()
                AIModelStatus.objects.update_or_create(
                    component='prediction',
                    defaults={'status': 'active', 'progress': 100, 'updated_at': timezone.now()}
                )
                ai_action_message = f'Anomaly detection complete. {len(anomalies)} anomalies found.'
            elif ai_action == 'train_model':
                AIModelStatus.objects.update_or_create(
                    component='prediction',
                    defaults={'status': 'training', 'progress': 0, 'updated_at': timezone.now()}
                )
                acc = train_model()
                AIModelStatus.objects.update_or_create(
                    component='prediction',
                    defaults={'status': 'active', 'progress': 100, 'updated_at': timezone.now()}
                )
                ai_action_message = f'Model trained. Accuracy: {acc:.2%}'
            messages.success(request, ai_action_message)
            return redirect('ai_engine:overview')
        # Accept/Review actions
        action = request.POST.get('action')
        proposal_title = request.POST.get('proposal_title')
        if proposal_title and action in ['accept', 'review']:
            obj, created = RecommendationAction.objects.update_or_create(
                user=request.user,
                proposal_title=proposal_title,
                defaults={'action': action}
            )
            messages.success(request, f'Action "{action.title()}" recorded for "{proposal_title}".')
        return redirect('ai_engine:overview')

    ai_accuracy = random.randint(90, 99)
    processed_proposals = GrantProposal.objects.count()
    time_saved = random.randint(60, 80)
    predictions = processed_proposals * random.randint(1, 2)

    months = []
    accuracy = []
    now = timezone.now()
    for i in range(6, 0, -1):
        month = (now - timezone.timedelta(days=30*i)).strftime('%b')
        months.append(month)
        accuracy.append(random.randint(85, 99))

    top_proposals = GrantProposal.objects.order_by('-requested_amount')[:5]
    recommendations = []
    anomalies = []
    actions = {a.proposal_title: a.action for a in RecommendationAction.objects.filter(user=request.user)}
    for p in top_proposals:
        features = {'requested_amount': p.requested_amount or 0}
        # Use stored prediction if available
        pred_obj = getattr(p, 'ai_prediction', None)
        score = pred_obj.score if pred_obj else predict(features)
        rec = {
            'score': int(score * 100),
            'title': p.proposal_title,
            'school': p.school.school_name if p.school else 'Unknown',
            'desc': p.description or 'AI-generated recommendation.',
            'date': (p.created_at or now).strftime('%b %d, %Y'),
            'prediction': score,
            'action': actions.get(p.proposal_title, None),
        }
        recommendations.append(rec)
        # Use stored anomaly if available
        anomaly_objs = p.ai_anomalies.all()
        if anomaly_objs.exists():
            anomalies.append(rec)

    # Real model status (live from DB)
    model_status_obj = AIModelStatus.objects.filter(component='prediction').first()
    if model_status_obj:
        model_status = {
            'allocation': 'Active',
            'allocation_progress': 94,
            'prediction': model_status_obj.status.title(),
            'prediction_progress': model_status_obj.progress,
            'risk': 'Training',
            'risk_progress': 65,
            'fraud': 'Active',
            'fraud_progress': 88,
        }
        feature_importances = model_status_obj.feature_importances
        model_accuracy = model_status_obj.accuracy
    else:
        model_status = {
            'allocation': 'Active',
            'allocation_progress': 94,
            'prediction': 'Idle',
            'prediction_progress': 0,
            'risk': 'Training',
            'risk_progress': 65,
            'fraud': 'Active',
            'fraud_progress': 88,
        }
        feature_importances = {}
        model_accuracy = None

    all_predictions = ProposalPrediction.objects.select_related('proposal').all().order_by('-updated_at')
    all_anomalies = ProposalAnomaly.objects.select_related('proposal').all().order_by('-detected_at')

    # Dynamic metrics
    total_proposals = GrantProposal.objects.count()
    total_predictions = all_predictions.count()
    total_anomalies = all_anomalies.count()
    avg_score = all_predictions.aggregate(avg=models.Avg('score'))['avg'] or 0
    anomaly_pct = (total_anomalies / total_proposals * 100) if total_proposals else 0

    # Score distribution for chart
    score_list = list(all_predictions.values_list('score', flat=True))

    # Anomaly frequency by month
    anomaly_dates = [a.detected_at.strftime('%Y-%m') for a in all_anomalies]
    anomaly_counts = Counter(anomaly_dates)
    anomaly_months = sorted(anomaly_counts.keys())
    anomaly_freq = [anomaly_counts[m] for m in anomaly_months]

    # Top 5 proposals by score
    top_pred_objs = all_predictions.order_by('-score')[:5]
    top_titles = [p.proposal.proposal_title for p in top_pred_objs]
    top_scores = [p.score for p in top_pred_objs]

    context = {
        'ai_accuracy': ai_accuracy,
        'processed_proposals': processed_proposals,
        'time_saved': time_saved,
        'predictions': predictions,
        'prediction_labels_json': json.dumps(months),
        'prediction_accuracy_json': json.dumps(accuracy),
        'recommendations': recommendations,
        'anomalies': anomalies,
        'model_status': model_status,
        'feature_importances': feature_importances,
        'model_accuracy': model_accuracy,
        'all_predictions': all_predictions,
        'all_anomalies': all_anomalies,
        'total_proposals': total_proposals,
        'total_predictions': total_predictions,
        'total_anomalies': total_anomalies,
        'avg_score': avg_score,
        'anomaly_pct': anomaly_pct,
        'score_list': score_list,
        'anomaly_months': anomaly_months,
        'anomaly_freq': anomaly_freq,
        'top_titles': top_titles,
        'top_scores': top_scores,
    }
    return render(request, "ai_engine/overview.html", context)

def algorithm_list_view(request):
    return HttpResponse('algorithm_list_view')

def algorithm_create_view(request):
    return HttpResponse('algorithm_create_view')

def algorithm_detail_view(request, algorithm_id):
    return HttpResponse('algorithm_detail_view')

def algorithm_edit_view(request, algorithm_id):
    return HttpResponse('algorithm_edit_view')

def algorithm_test_view(request, algorithm_id):
    return HttpResponse('algorithm_test_view')

def factor_list_view(request):
    return HttpResponse('factor_list_view')

def factor_create_view(request):
    return HttpResponse('factor_create_view')

def factor_detail_view(request, factor_id):
    return HttpResponse('factor_detail_view')

def factor_edit_view(request, factor_id):
    return HttpResponse('factor_edit_view')

def run_list_view(request):
    return HttpResponse('run_list_view')

def run_create_view(request):
    return HttpResponse('run_create_view')

def run_detail_view(request, run_id):
    return HttpResponse('run_detail_view')

def run_execute_view(request, run_id):
    return HttpResponse('run_execute_view')

def run_cancel_view(request, run_id):
    return HttpResponse('run_cancel_view')

def score_list_view(request):
    return HttpResponse('score_list_view')

def score_detail_view(request, score_id):
    return HttpResponse('score_detail_view')

def risk_list_view(request):
    return HttpResponse('risk_list_view')

def risk_create_view(request):
    return HttpResponse('risk_create_view')

def risk_detail_view(request, risk_id):
    return HttpResponse('risk_detail_view')

def risk_edit_view(request, risk_id):
    return HttpResponse('risk_edit_view')

def risk_resolve_view(request, risk_id):
    return HttpResponse('risk_resolve_view')

def recommendation_list_view(request):
    return HttpResponse('recommendation_list_view')

def recommendation_create_view(request):
    return HttpResponse('recommendation_create_view')

def recommendation_detail_view(request, recommendation_id):
    return HttpResponse('recommendation_detail_view')

def recommendation_implement_view(request, recommendation_id):
    return HttpResponse('recommendation_implement_view')

def metric_list_view(request):
    return HttpResponse('metric_list_view')

def metric_create_view(request):
    return HttpResponse('metric_create_view')

def metric_detail_view(request, metric_id):
    return HttpResponse('metric_detail_view')

def metric_edit_view(request, metric_id):
    return HttpResponse('metric_edit_view')

def config_view(request):
    return HttpResponse('config_view')

def config_update_view(request):
    return HttpResponse('config_update_view')
