from django.contrib import admin
from .models import Loan

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('loan_id', 'user', 'amount', 'tenure', 'interest_rate', 'status', 'created_at')
    search_fields = ('loan_id', 'user__username')
    list_filter = ('status', 'created_at')
