import random
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    otp = models.CharField(max_length=6, blank=True, null=True)  # OTP Field
    is_verified = models.BooleanField(default=False)

    def generate_otp(self):
        """Generate a random 6-digit OTP and save it."""
        self.otp = str(random.randint(100000, 999999))
        self.save()

