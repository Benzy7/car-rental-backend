from django.db import models
from .base import TimestampedModel
from .user import User
from .car import Car

class CarBooking(TimestampedModel):
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, related_name="bookings", null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    car_title = models.CharField(max_length=100)
    user_email = models.EmailField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Booking for {self.car.car_model.name} by {self.user.username} from {self.start_date} to {self.end_date}"
