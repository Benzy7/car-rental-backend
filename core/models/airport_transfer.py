from django.db import models
from .base import TimestampedModel

class Airport(TimestampedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class TransferDestination(TimestampedModel):
    airport = models.ForeignKey(Airport, related_name="transfer_destinations", on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.city} - {self.price} DT"
