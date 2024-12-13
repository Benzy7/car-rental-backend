from django.db import models
from core.models.base import TimestampedModel
from core.models.user import User

#TODO
class Location(TimestampedModel):
    title = models.CharField(max_length=100)    
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    user = models.ForeignKey(User, related_name="locations", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_location_type_display()} - {self.address or 'No address'}"
