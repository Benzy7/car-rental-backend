import uuid
from django.db import models
from .base import TimestampedModel
from .user import User
from .car import Car
from .coupon import Coupon
from .airport_transfer import Airport, TransferDestination

class BookingStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'

class BookingType(models.TextChoices):
    STANDARD = 'standard', 'Standard'
    EVENT = 'event', 'Event'
    TRANSFER = 'transfer', 'Transfer'

class CarBooking(TimestampedModel):
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, related_name="bookings", null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    car_description = models.CharField(max_length=100, blank=True)
    user_email = models.EmailField()
    
    booking_type = models.CharField(max_length=10, choices=BookingType.choices)
    status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.PENDING)
    cancel_reason = models.CharField(max_length=255, blank=True)
    cancelled_date = models.DateTimeField(null=True)
    confirmed_date = models.DateTimeField(null=True)
    
    start_date = models.DateField()
    end_date = models.DateField()
    pickup_time = models.TimeField(null=True)
    return_time = models.TimeField(null=True)
    
    flight_number = models.CharField(max_length=20, blank=True)
    plane_arrival_datetime = models.DateTimeField(null=True)
    airport = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True)
    transfer_destination = models.ForeignKey(TransferDestination, on_delete=models.SET_NULL, null=True)
    transfer_description  = models.CharField(max_length=255, blank=True)
 
    with_driver = models.BooleanField(default=False)
    driver_name = models.CharField(max_length=100, blank=True)
    driver_contact = models.CharField(max_length=20, blank=True)
    
    with_delivery = models.BooleanField(default=False)       
    car_pickup_location = models.CharField(max_length=200, blank=True)
    car_return_location = models.CharField(max_length=200, blank=True)
    
    phone_number_1 = models.CharField(max_length=15, blank=True)
    phone_number_2 = models.CharField(max_length=15, blank=True)
    additional_notes = models.TextField(blank=True)
    
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True)
    coupon_code = models.CharField(max_length=8, blank=True)
    
    coupon_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    normal_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    features_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    transfer_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    driver_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    final_total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    qr_code = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.qr_code = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking for {self.car.car_model.name if self.car else self.car_description} by {self.user_email} from {self.start_date} to {self.end_date}"
