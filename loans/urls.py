from django.urls import path
from .views import LoanListCreateView, LoanDetailView, LoanForeclosureView, AdminLoanListView, AdminLoanDetailView

urlpatterns = [
    path('loans/', LoanListCreateView.as_view(), name='loan-list-create'),
    path('loans/<int:pk>/', LoanDetailView.as_view(), name='loan-detail'),
    path('loans/<int:pk>/foreclose/', LoanForeclosureView.as_view(), name='loan-foreclosure'),
    

    # Admin Loan Management
    path('admin/loans/', AdminLoanListView.as_view(), name='admin-loan-list'),
    path('admin/loans/<int:pk>/', AdminLoanDetailView.as_view(), name='admin-loan-detail'),
]