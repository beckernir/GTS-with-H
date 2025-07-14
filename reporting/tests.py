from django.test import TestCase
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import User, School
from reporting.models import Report, KPI, KPIValue, AnalyticsEvent, DataExport
from budget.models import SchoolBudget, BudgetPeriod, BudgetReport
import random
import uuid
from datetime import timedelta

# Create your tests here.
