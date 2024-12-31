from django.db import models
from .base import TimestampedModel
from .car_booking import CarBooking

# TODO: not applicable to all cars!
class CarFeature(TimestampedModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    is_active = models.BooleanField(default=True)

class BookingFeature(TimestampedModel):
    booking = models.ForeignKey(CarBooking, on_delete=models.CASCADE, related_name="features")
    feature = models.ForeignKey(CarFeature, on_delete=models.CASCADE, related_name="applied_bookings")
    price = models.DecimalField(max_digits=10, decimal_places=2)
