from django.db import models
from users.models import User
from decimal import Decimal
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta

class Loan(models.Model):
    loan_id = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_interest = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=10, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_loan_details(self):
        monthly_rate = self.interest_rate / 100 / 12
        self.total_interest = self.amount * ((1 + monthly_rate) ** self.tenure - 1)
        self.total_amount = self.amount + self.total_interest
        self.monthly_installment = self.total_amount / self.tenure
        self.save()

    def generate_payment_schedule(self):
        from datetime import timedelta
        from django.utils.timezone import now
        for i in range(1, self.tenure + 1):
            PaymentSchedule.objects.create(
                loan=self,
                installment_no=i,
                due_date=now().date() + timedelta(days=30 * i),
                amount=self.monthly_installment,
                status="PENDING"
            )

    def foreclose(self):
        remaining_principal = self.total_amount - (self.monthly_installment * (self.tenure - 1))
        foreclosure_discount = remaining_principal * Decimal(0.05) 
        final_settlement_amount = remaining_principal - foreclosure_discount
        self.total_amount = final_settlement_amount
        self.status = 'CLOSED'
        self.save()
        return {
            "loan_id": self.loan_id,
            "amount_paid": self.total_amount,
            "foreclosure_discount": foreclosure_discount,
            "final_settlement_amount": final_settlement_amount,
            "status": self.status
        }


class PaymentSchedule(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payment_schedule')
    installment_no = models.IntegerField()
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=[('PAID', 'Paid'), ('PENDING', 'Pending')], default='PENDING')
