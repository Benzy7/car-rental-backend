from .base import TimestampedModel, COUNTRY_CHOICES
from django.db import models
from django.utils.text import slugify
from core.models.user import User

class Partner(TimestampedModel):
    class PartnerType(models.TextChoices):
        TRAVEL_AGENCY = 'travel_agency', 'Travel Agency'
        CAR_RENTAL = 'car_rental', 'Car Rental'
        EVENT_PLANNER = 'event_planner', 'Event Planner'

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    partner_type = models.CharField(max_length=50, choices=PartnerType.choices)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    manager = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES, blank=True)  

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.name} - {self.get_partner_type_display()}"
