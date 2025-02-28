from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from .models import User
from .utils import send_otp_email

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.generate_otp()  # Generate OTP
            send_otp_email(user.email, user.otp)  # Send OTP via email
            return Response({"message": "OTP sent to email. Verify to activate your account."})
        return Response(serializer.errors)
    

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            user = User.objects.get(email=email, otp=otp)
            user.is_verified = True  # Mark user as verified
            user.otp = None  # Clear OTP after successful verification
            user.save()
            return Response({"message": "Account verified successfully."})
        except User.DoesNotExist:
            return Response({"error": "Invalid OTP or email."})

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            if not user.is_verified:
                return Response({'error': 'Account not verified. Check your email for OTP.'})
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
        return Response({'error': 'Invalid credentials'})
