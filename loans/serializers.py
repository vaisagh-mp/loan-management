from rest_framework import serializers
from .models import Loan, PaymentSchedule

class PaymentScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentSchedule
        fields = ['installment_no', 'due_date', 'amount', 'status']


class LoanSerializer(serializers.ModelSerializer):
    payment_schedule = PaymentScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ['loan_id', 'user', 'status', 'created_at']

    def create(self, validated_data):
        # Auto-generate loan_id
        validated_data['loan_id'] = f"LOAN{Loan.objects.count() + 1:03d}"
        return super().create(validated_data)
