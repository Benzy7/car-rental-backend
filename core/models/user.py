from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from core.models.base import TimestampedModel

def upload_profile_picture(instance, filename):
    return f"{settings.FILES_FOLDER}/users/{instance.id}/profile_picture/{filename}"

def upload_passport_picture(instance, filename):
    return f"{settings.FILES_FOLDER}/users/{instance.id}/passport/{filename}"

def upload_driver_licence_1(instance, filename):
    return f"{settings.FILES_FOLDER}/users/{instance.id}/driver_licence/1_{filename}"

def upload_driver_licence_2(instance, filename):
    return f"{settings.FILES_FOLDER}/users/{instance.id}/driver_licence/1_{filename}"

class Role(models.TextChoices):
    CLIENT = 'client', 'Client'
    PARTNER = 'partner', 'Partner'
    ADMIN = 'admin', 'Admin'

class Gender(models.TextChoices):
    FEMALE = 'female', 'Female'
    MALE = 'male', 'Male'
    NOT_SPECIFIED = 'not_specified', 'Prefer not to say'

class User(AbstractUser, TimestampedModel):
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=10, 
        choices=Role.choices, 
        default=Role.CLIENT
    )
    
    gender = models.CharField(
        max_length=15,
        choices=Gender.choices,
        blank=True,
        default=Gender.NOT_SPECIFIED
    )
    birthday = models.DateField(null=True, blank=True)
    
    country = models.CharField(max_length=100, blank=True)  
    phone_number = models.CharField(max_length=15, blank=True)
    phone_country_code = models.CharField(max_length=5, blank=True)  
    
    profile_picture = models.ImageField(upload_to=upload_profile_picture, null=True)
    passport_picture = models.ImageField(upload_to=upload_passport_picture, null=True)
    driver_licence_picture_1 = models.ImageField(upload_to=upload_driver_licence_1, null=True)
    driver_licence_picture_2 = models.ImageField(upload_to=upload_driver_licence_2, null=True)
    
    is_complete = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_blacklisted = models.BooleanField(default=False)  
    blacklist_reason = models.CharField(max_length=255, blank=True)    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    username = None
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
