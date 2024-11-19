
from django.db import models
from core.models.base import TimestampedModel
from .user import User
from django.utils import timezone
from datetime import timedelta

class PinCode(TimestampedModel):
    RESET_PASSWORD = 'reset_password'
    PIN_TYPE_CHOICES = [
        (RESET_PASSWORD, 'Reset Password'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6) 
    code_type = models.CharField(max_length=50, choices=PIN_TYPE_CHOICES)
    is_used = models.BooleanField(default=False)
    
    def is_expired(self, expiration_minutes=15):
        return timezone.now() > self.created_at + timedelta(minutes=expiration_minutes)
