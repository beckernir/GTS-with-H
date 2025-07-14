from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from core.models import User, School
from grants.models import GrantProposal, GrantCategory
import uuid
from django.conf import settings


class AllocationAlgorithm(models.Model):
    """
    Model for storing different AI allocation algorithms and their configurations.
    """
    
    # Algorithm types
    ALGORITHM_TYPE_CHOICES = [
        ('weighted_scoring', 'Weighted Scoring'),
        ('machine_learning', 'Machine Learning'),
        ('optimization', 'Optimization Algorithm'),
        ('rule_based', 'Rule-Based System'),
        ('hybrid', 'Hybrid Approach'),
    ]
    
    # Core fields
    algorithm_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    algorithm_name = models.CharField(max_length=100, unique=True)
    algorithm_type = models.CharField(max_length=20, choices=ALGORITHM_TYPE_CHOICES, default='weighted_scoring')
    description = models.TextField()
    
    # Algorithm configuration
    configuration = models.JSONField(default=dict, help_text="JSON object containing algorithm parameters")
    version = models.CharField(max_length=20, default='1.0.0')
    
    # Algorithm status
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    
    # Performance metrics
    accuracy_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Algorithm accuracy (0-100)")
    last_updated = models.DateTimeField(auto_now=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_algorithms')
    
    class Meta:
        db_table = 'ai_engine_allocation_algorithm'
        verbose_name = 'Allocation Algorithm'
        verbose_name_plural = 'Allocation Algorithms'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.algorithm_name} v{self.version}"


class AllocationFactor(models.Model):
    """
    Model for defining factors used in AI allocation decisions.
    """
    
    # Factor categories
    FACTOR_CATEGORY_CHOICES = [
        ('school_performance', 'School Performance'),
        ('need_assessment', 'Need Assessment'),
        ('geographic', 'Geographic Factors'),
        ('demographic', 'Demographic Factors'),
        ('historical', 'Historical Data'),
        ('compliance', 'Compliance Factors'),
        ('impact_potential', 'Impact Potential'),
        ('other', 'Other Factors'),
    ]
    
    # Factor types
    FACTOR_TYPE_CHOICES = [
        ('numeric', 'Numeric Score'),
        ('percentage', 'Percentage'),
        ('boolean', 'Boolean (Yes/No)'),
        ('categorical', 'Categorical'),
        ('weighted', 'Weighted Score'),
    ]
    
    # Core fields
    factor_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    factor_name = models.CharField(max_length=100, unique=True)
    factor_category = models.CharField(max_length=20, choices=FACTOR_CATEGORY_CHOICES, default='other')
    factor_type = models.CharField(max_length=20, choices=FACTOR_TYPE_CHOICES, default='numeric')
    
    # Factor configuration
    description = models.TextField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=1.00, help_text="Factor weight in allocation (0.00-1.00)")
    min_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_value = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    
    # Factor settings
    is_active = models.BooleanField(default=True)
    is_required = models.BooleanField(default=False)
    auto_calculate = models.BooleanField(default=True, help_text="Whether factor is calculated automatically")
    
    # Calculation method
    calculation_formula = models.TextField(blank=True, null=True, help_text="Formula or method for calculating this factor")
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_factors')
    
    class Meta:
        db_table = 'ai_engine_allocation_factor'
        verbose_name = 'Allocation Factor'
        verbose_name_plural = 'Allocation Factors'
        ordering = ['factor_category', 'factor_name']
    
    def __str__(self):
        return f"{self.factor_name} ({self.get_factor_category_display()})"


class AllocationRun(models.Model):
    """
    Model for tracking AI allocation runs and their results.
    """
    
    # Run status choices
    RUN_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Core fields
    run_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    run_name = models.CharField(max_length=200)
    algorithm = models.ForeignKey(AllocationAlgorithm, on_delete=models.CASCADE, related_name='allocation_runs')
    
    # Run scope
    total_proposals = models.PositiveIntegerField(default=0)
    total_budget_available = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_allocated = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    # Run status and timing
    status = models.CharField(max_length=20, choices=RUN_STATUS_CHOICES, default='pending')
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    
    # Run configuration
    configuration = models.JSONField(default=dict, help_text="JSON object containing run parameters")
    results_summary = models.JSONField(default=dict, help_text="JSON object containing run results summary")
    
    # Error handling
    error_message = models.TextField(blank=True, null=True)
    error_details = models.JSONField(default=dict, help_text="JSON object containing error details")
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiated_allocation_runs')
    
    class Meta:
        db_table = 'ai_engine_allocation_run'
        verbose_name = 'Allocation Run'
        verbose_name_plural = 'Allocation Runs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.run_name} - {self.get_status_display()}"
    
    def get_duration_formatted(self):
        """Get formatted duration string."""
        if self.duration_seconds:
            minutes = self.duration_seconds // 60
            seconds = self.duration_seconds % 60
            return f"{minutes}m {seconds}s"
        return "0s"


class ProposalAllocationScore(models.Model):
    """
    Model for storing AI-calculated allocation scores for individual proposals.
    """
    
    # Core fields
    score_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    allocation_run = models.ForeignKey(AllocationRun, on_delete=models.CASCADE, related_name='proposal_scores')
    proposal = models.ForeignKey(GrantProposal, on_delete=models.CASCADE, related_name='allocation_scores')
    
    # Score details
    total_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Overall allocation score (0-100)")
    rank = models.PositiveIntegerField(default=0, help_text="Ranking position in allocation run")
    
    # Factor scores
    factor_scores = models.JSONField(default=dict, help_text="JSON object containing individual factor scores")
    
    # Allocation recommendation
    recommended_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    allocation_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Percentage of requested amount recommended")
    
    # Decision tracking
    is_allocated = models.BooleanField(default=False)
    allocated_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    allocation_date = models.DateTimeField(blank=True, null=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ai_engine_proposal_allocation_score'
        verbose_name = 'Proposal Allocation Score'
        verbose_name_plural = 'Proposal Allocation Scores'
        ordering = ['allocation_run', '-total_score']
        unique_together = ['allocation_run', 'proposal']
    
    def __str__(self):
        return f"{self.proposal.proposal_title} - Score: {self.total_score}"


class RiskAssessment(models.Model):
    """
    Model for AI-driven risk assessment of proposals and schools.
    """
    
    # Risk levels
    RISK_LEVEL_CHOICES = [
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
        ('critical', 'Critical Risk'),
    ]
    
    # Risk categories
    RISK_CATEGORY_CHOICES = [
        ('financial', 'Financial Risk'),
        ('compliance', 'Compliance Risk'),
        ('operational', 'Operational Risk'),
        ('reputational', 'Reputational Risk'),
        ('strategic', 'Strategic Risk'),
        ('other', 'Other Risk'),
    ]
    
    # Core fields
    risk_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    risk_name = models.CharField(max_length=200)
    risk_category = models.CharField(max_length=20, choices=RISK_CATEGORY_CHOICES, default='other')
    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES, default='low')
    
    # Risk assessment scope
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='risk_assessments', null=True, blank=True)
    proposal = models.ForeignKey(GrantProposal, on_delete=models.CASCADE, related_name='risk_assessments', null=True, blank=True)
    
    # Risk details
    description = models.TextField()
    risk_factors = models.JSONField(default=dict, help_text="JSON object containing risk factors and scores")
    risk_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Overall risk score (0-100)")
    
    # Mitigation and monitoring
    mitigation_strategies = models.TextField(blank=True, null=True)
    monitoring_requirements = models.TextField(blank=True, null=True)
    
    # Risk status
    is_active = models.BooleanField(default=True)
    is_resolved = models.BooleanField(default=False)
    resolution_date = models.DateTimeField(blank=True, null=True)
    resolution_notes = models.TextField(blank=True, null=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_risk_assessments')
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_risk_assessments')
    
    class Meta:
        db_table = 'ai_engine_risk_assessment'
        verbose_name = 'Risk Assessment'
        verbose_name_plural = 'Risk Assessments'
        ordering = ['-risk_score', '-created_at']
    
    def __str__(self):
        return f"{self.risk_name} - {self.get_risk_level_display()}"


class OptimizationRecommendation(models.Model):
    """
    Model for AI-generated optimization recommendations.
    """
    
    # Recommendation types
    RECOMMENDATION_TYPE_CHOICES = [
        ('budget_optimization', 'Budget Optimization'),
        ('process_improvement', 'Process Improvement'),
        ('resource_allocation', 'Resource Allocation'),
        ('risk_mitigation', 'Risk Mitigation'),
        ('performance_enhancement', 'Performance Enhancement'),
        ('compliance_improvement', 'Compliance Improvement'),
        ('other', 'Other'),
    ]
    
    # Priority levels
    PRIORITY_CHOICES = [
        ('low', 'Low Priority'),
        ('medium', 'Medium Priority'),
        ('high', 'High Priority'),
        ('urgent', 'Urgent'),
    ]
    
    # Core fields
    recommendation_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    recommendation_type = models.CharField(max_length=30, choices=RECOMMENDATION_TYPE_CHOICES, default='other')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Recommendation scope
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='optimization_recommendations', null=True, blank=True)
    proposal = models.ForeignKey(GrantProposal, on_delete=models.CASCADE, related_name='optimization_recommendations', null=True, blank=True)
    
    # Recommendation details
    title = models.CharField(max_length=200)
    description = models.TextField()
    rationale = models.TextField(help_text="AI reasoning behind the recommendation")
    
    # Expected impact
    expected_impact = models.TextField()
    impact_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Expected impact score (0-100)")
    
    # Implementation details
    implementation_steps = models.JSONField(default=list, help_text="JSON array containing implementation steps")
    estimated_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    estimated_duration_days = models.PositiveIntegerField(default=0)
    
    # Recommendation status
    is_implemented = models.BooleanField(default=False)
    implementation_date = models.DateTimeField(blank=True, null=True)
    implementation_notes = models.TextField(blank=True, null=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_recommendations')
    implemented_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='implemented_recommendations')
    
    class Meta:
        db_table = 'ai_engine_optimization_recommendation'
        verbose_name = 'Optimization Recommendation'
        verbose_name_plural = 'Optimization Recommendations'
        ordering = ['-priority', '-impact_score', '-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_priority_display()}"


class AIPerformanceMetrics(models.Model):
    """
    Model for tracking AI system performance and accuracy metrics.
    """
    
    # Metric types
    METRIC_TYPE_CHOICES = [
        ('allocation_accuracy', 'Allocation Accuracy'),
        ('prediction_accuracy', 'Prediction Accuracy'),
        ('risk_detection', 'Risk Detection'),
        ('optimization_effectiveness', 'Optimization Effectiveness'),
        ('system_performance', 'System Performance'),
        ('user_satisfaction', 'User Satisfaction'),
    ]
    
    # Core fields
    metric_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    metric_type = models.CharField(max_length=30, choices=METRIC_TYPE_CHOICES, default='allocation_accuracy')
    metric_name = models.CharField(max_length=100)
    
    # Metric values
    metric_value = models.DecimalField(max_digits=10, decimal_places=4, default=0.0000)
    target_value = models.DecimalField(max_digits=10, decimal_places=4, default=0.0000)
    threshold_value = models.DecimalField(max_digits=10, decimal_places=4, default=0.0000)
    
    # Metric context
    measurement_date = models.DateField()
    measurement_period = models.CharField(max_length=50, help_text="e.g., '2024 Q1', 'Monthly', 'Weekly'")
    
    # Performance tracking
    is_above_target = models.BooleanField(default=False)
    is_above_threshold = models.BooleanField(default=False)
    trend_direction = models.CharField(max_length=10, choices=[('up', 'Up'), ('down', 'Down'), ('stable', 'Stable')], default='stable')
    
    # Additional data
    metadata = models.JSONField(default=dict, help_text="JSON object containing additional metric data")
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ai_engine_ai_performance_metrics'
        verbose_name = 'AI Performance Metric'
        verbose_name_plural = 'AI Performance Metrics'
        ordering = ['-measurement_date', 'metric_type']
    
    def __str__(self):
        return f"{self.metric_name} - {self.metric_value} ({self.measurement_period})"
    
    def get_performance_status(self):
        """Get performance status based on target and threshold."""
        if self.metric_value >= self.target_value:
            return "excellent"
        elif self.metric_value >= self.threshold_value:
            return "good"
        else:
            return "needs_improvement"


class RecommendationAction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    proposal_title = models.CharField(max_length=255)
    action = models.CharField(max_length=20, choices=[('accept', 'Accept'), ('review', 'Review')])
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'proposal_title')

    def __str__(self):
        return f"{self.user} - {self.proposal_title} - {self.action}"


class AIModelStatus(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('training', 'Training'),
        ('idle', 'Idle'),
        ('error', 'Error'),
    ]
    component = models.CharField(max_length=50, unique=True)  # e.g., 'allocation', 'prediction', 'risk', 'fraud'
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='idle')
    progress = models.PositiveIntegerField(default=0)
    accuracy = models.FloatField(default=0.0)
    feature_importances = models.JSONField(default=dict, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.component} - {self.status} ({self.progress}%)"


class ProposalPrediction(models.Model):
    proposal = models.OneToOneField(GrantProposal, on_delete=models.CASCADE, related_name='ai_prediction')
    score = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.proposal.proposal_title}: {self.score:.2f}"


class ProposalAnomaly(models.Model):
    proposal = models.ForeignKey(GrantProposal, on_delete=models.CASCADE, related_name='ai_anomalies')
    anomaly_type = models.CharField(max_length=50, default='score')
    score = models.FloatField()
    detected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.proposal.proposal_title}: {self.anomaly_type} ({self.score:.2f})"
