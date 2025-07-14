from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'schools', views.SchoolViewSet)
router.register(r'grant-proposals', views.GrantProposalViewSet)
router.register(r'grant-categories', views.GrantCategoryViewSet)
router.register(r'school-budgets', views.SchoolBudgetViewSet)
router.register(r'training-courses', views.TrainingCourseViewSet)
router.register(r'community-forums', views.CommunityForumViewSet)
router.register(r'kpis', views.KPIViewSet)
router.register(r'allocations', views.AllocationRunViewSet)

urlpatterns = [
    # API root
    path('root/', views.api_root, name='api_root'),
    
    # Include router URLs
    path('', include(router.urls)),
    
    # Custom API endpoints
    path('dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),
    path('grants/ai-allocation/', views.ai_allocation, name='ai_allocation'),
    path('reports/generate/', views.generate_report, name='generate_report'),
    path('analytics/events/', views.analytics_events, name='analytics_events'),
    
    # Authentication endpoints
    path('auth/', include('rest_framework.urls')),
] 