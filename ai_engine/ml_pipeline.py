import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from ai_engine.models import AIModelStatus, ProposalPrediction, ProposalAnomaly
from django.utils import timezone
from grants.models import GrantProposal

DATA_PATH = 'ai_engine/dataset/training_data.csv'
MODEL_PATH = 'ai_engine/dataset/model.joblib'

FEATURES = [
    'requested_amount',
    # Add more features as needed
]
TARGET = 'status'

STATUS_MAP = {
    'approved': 1,
    'completed': 1,
    'closed': 1,
    'rejected': 0,
    'pending': 0,
    'submitted': 0,
    'draft': 0,
    'cancelled': 0,
}

def load_data():
    df = pd.read_csv(DATA_PATH)
    # Convert status to binary
    df['status_bin'] = df['status'].map(STATUS_MAP).fillna(0).astype(int)
    df = df.dropna(subset=FEATURES)
    return df

def train_model():
    df = load_data()
    X = df[FEATURES]
    y = df['status_bin']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    joblib.dump(model, MODEL_PATH)
    # Save status and feature importances
    importances = dict(zip(FEATURES, model.feature_importances_))
    AIModelStatus.objects.update_or_create(
        component='prediction',
        defaults={
            'status': 'active',
            'progress': 100,
            'accuracy': acc,
            'feature_importances': importances,
            'updated_at': timezone.now(),
        }
    )
    return acc

def load_model():
    if not os.path.exists(MODEL_PATH):
        train_model()
    return joblib.load(MODEL_PATH)

def predict(features_dict):
    model = load_model()
    X = np.array([[features_dict.get(f, 0) for f in FEATURES]])
    proba = model.predict_proba(X)[0][1]  # Probability of positive class
    return proba

def generate_predictions():
    proposals = GrantProposal.objects.all()
    model = load_model()
    total = proposals.count()
    created = 0
    for i, p in enumerate(proposals, 1):
        features = {f: getattr(p, f, 0) or 0 for f in FEATURES}
        score = model.predict_proba(np.array([[features.get(f, 0) for f in FEATURES]]))[0][1]
        obj, _ = ProposalPrediction.objects.update_or_create(
            proposal=p,
            defaults={'score': score}
        )
        created += 1
        # Update progress
        AIModelStatus.objects.update_or_create(
            component='prediction',
            defaults={
                'status': 'active',
                'progress': int(i / total * 100),
                'updated_at': timezone.now(),
            }
        )
    print(f"Predictions created: {created} for {total} proposals")
    AIModelStatus.objects.update_or_create(
        component='prediction',
        defaults={
            'status': 'active',
            'progress': 100,
            'updated_at': timezone.now(),
        }
    )
    return total

def detect_anomalies():
    proposals = GrantProposal.objects.all()
    model = load_model()
    anomalies = []
    total = proposals.count()
    created = 0
    for i, p in enumerate(proposals, 1):
        features = {f: getattr(p, f, 0) or 0 for f in FEATURES}
        score = model.predict_proba(np.array([[features.get(f, 0) for f in FEATURES]]))[0][1]
        if score < 0.2 or score > 0.95:
            ProposalAnomaly.objects.create(
                proposal=p,
                anomaly_type='score',
                score=score
            )
            anomalies.append(p.id)
            created += 1
        # Update progress
        AIModelStatus.objects.update_or_create(
            component='prediction',
            defaults={
                'status': 'active',
                'progress': int(i / total * 100),
                'updated_at': timezone.now(),
            }
        )
    print(f"Anomalies created: {created} for {total} proposals")
    AIModelStatus.objects.update_or_create(
        component='prediction',
        defaults={
            'status': 'active',
            'progress': 100,
            'updated_at': timezone.now(),
        }
    )
    return anomalies 