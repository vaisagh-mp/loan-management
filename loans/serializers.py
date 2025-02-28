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

    def validate_amount(self, value):
        if value < 1000 or value > 100000:
            raise serializers.ValidationError("Loan amount must be between ₹1,000 and ₹100,000.")
        return value

    def validate_tenure(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError("Tenure must be a whole number.")
        if value < 3 or value > 24:
            raise serializers.ValidationError("Tenure must be between 3 and 24 months.")
        return value

    def create(self, validated_data):
        # Auto-generate loan_id
        validated_data['loan_id'] = f"LOAN{Loan.objects.count() + 1:03d}"
        return super().create(validated_data)