from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import Loan
from .serializers import LoanSerializer

class LoanListCreateView(ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        loan = serializer.save(user=self.request.user)
        loan.calculate_loan_details()
        loan.generate_payment_schedule()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoanDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

class LoanForeclosureView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            loan = Loan.objects.get(pk=pk, user=request.user)
            response_data = loan.foreclose()
            return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)

class AdminLoanListView(ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAdminUser]


class AdminLoanDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAdminUser]
