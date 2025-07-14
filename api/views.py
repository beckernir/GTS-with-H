from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import api_view
from django.http import HttpResponse

from core.models import User, School
from grants.models import GrantProposal, GrantCategory
from budget.models import SchoolBudget
from training.models import TrainingCourse
from community.models import CommunityForum
from reporting.models import KPI
from ai_engine.models import AllocationRun

# Create your views here.

class UserViewSet(ViewSet):
    queryset = User.objects.all()
    def list(self, request):
        return Response({'message': 'UserViewSet list'})

class SchoolViewSet(ViewSet):
    queryset = School.objects.all()
    def list(self, request):
        return Response({'message': 'SchoolViewSet list'})

class GrantProposalViewSet(ViewSet):
    queryset = GrantProposal.objects.all()
    def list(self, request):
        return Response({'message': 'GrantProposalViewSet list'})

class GrantCategoryViewSet(ViewSet):
    queryset = GrantCategory.objects.all()
    def list(self, request):
        return Response({'message': 'GrantCategoryViewSet list'})

class SchoolBudgetViewSet(ViewSet):
    queryset = SchoolBudget.objects.all()
    def list(self, request):
        return Response({'message': 'SchoolBudgetViewSet list'})

class TrainingCourseViewSet(ViewSet):
    queryset = TrainingCourse.objects.all()
    def list(self, request):
        return Response({'message': 'TrainingCourseViewSet list'})

class CommunityForumViewSet(ViewSet):
    queryset = CommunityForum.objects.all()
    def list(self, request):
        return Response({'message': 'CommunityForumViewSet list'})

class KPIViewSet(ViewSet):
    queryset = KPI.objects.all()
    def list(self, request):
        return Response({'message': 'KPIViewSet list'})

class AllocationRunViewSet(ViewSet):
    queryset = AllocationRun.objects.all()
    def list(self, request):
        return Response({'message': 'AllocationRunViewSet list'})

@api_view(['GET'])
def api_root(request):
    return Response({'message': 'API Root'})

@api_view(['GET'])
def dashboard_stats(request):
    return Response({'message': 'dashboard_stats'})

@api_view(['GET'])
def ai_allocation(request):
    return Response({'message': 'ai_allocation'})

@api_view(['GET'])
def generate_report(request):
    return Response({'message': 'generate_report'})

@api_view(['GET'])
def analytics_events(request):
    return Response({'message': 'analytics_events'})