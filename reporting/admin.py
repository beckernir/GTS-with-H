from django.contrib import admin
from .models import REBGrantBudget
from .models import ProposalCriterion, SupplierCriterion

# Register your models here.

admin.site.register(REBGrantBudget)
admin.site.register(ProposalCriterion)
admin.site.register(SupplierCriterion)
