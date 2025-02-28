from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Loan

User = get_user_model()

class LoanAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.admin = User.objects.create_superuser(username="admin", password="adminpass")

        self.client.login(username="testuser", password="testpass")
        self.user_token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')

        self.admin_token = str(RefreshToken.for_user(self.admin).access_token)

        self.loan_data = {
            "amount": 10000,
            "tenure": 12,
            "interest_rate": 10
        }


    def test_foreclose_loan(self):
        response = self.client.post("/api/loans/", self.loan_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
        loan = Loan.objects.first()
        self.assertIsNotNone(loan, "Loan object was not created")
    
        foreclosure_response = self.client.post(f"/api/loans/{loan.id}/foreclose/")
        self.assertEqual(foreclosure_response.status_code, status.HTTP_200_OK)
        self.assertEqual(foreclosure_response.data["status"], "success")
    
    def test_admin_view_loans(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
    
        response = self.client.get("/api/admin/loans/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_create_loan(self):
        response = self.client.post("/api/loans/", self.loan_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Loan.objects.count(), 1)
    