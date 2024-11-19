from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from core.models.base import TimestampedModel

def upload_profile_picture(instance, filename):
    return f"{settings.FILES_FOLDER}/profile_pictures/{filename}"

class User(AbstractUser, TimestampedModel):
    CLIENT = 'client'
    PARTNER = 'partner'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (CLIENT, 'Client'),
        (PARTNER, 'Partner'),
        (ADMIN, 'Admin'),
    ]

    GENDER_CHOICES = [
        ('female', 'Female'),
        ('male', 'Male'),
        ('other', 'Other'),
        ('not_specified', 'Prefer not to say'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default=CLIENT
    )
    phone_number = models.CharField(max_length=8, blank=True)
    gender = models.CharField(
        max_length=15,
        choices=GENDER_CHOICES,
        blank=True,
        default='not_specified'
    )
    is_profile_complete = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to=upload_profile_picture, null=True)
        
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    username = None

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
