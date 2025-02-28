from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(email, otp):
    subject = "Your OTP for Account Verification"
    message = f"Your OTP for account verification is: {otp}"
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])
