from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils import timezone
from django.conf import settings
from core.models.base import TimestampedModel
from core.models.partner import Partner

def upload_make_logo(instance, filename):
    return f"{settings.FILES_FOLDER}/makes/logos/{filename}"

def upload_car_image(instance, filename):
    return f"{settings.FILES_FOLDER}/cars/images/{instance.id}/{filename}"

class CarType(models.TextChoices):
    SUV = 'SUV', 'SUV'
    SEDAN = 'Sedan', 'Sedan'
    VAN = 'Van', 'Van'
    HATCHBACK = 'Hatchback', 'Hatchback'
    CONVERTIBLE = 'Convertible', 'Convertible'
    
class TransmissionType(models.TextChoices):
    MANUAL = 'Manual', 'Manual'
    AUTOMATIC = 'Automatic', 'Automatic'
    # SEMI_AUTOMATIC = 'Semi-automatic', 'Semi-automatic'

class FuelType(models.TextChoices):
    PETROL = 'Petrol', 'Petrol'
    DIESEL = 'Diesel', 'Diesel'
    ELECTRIC = 'Electric', 'Electric'
    HYBRID = 'Hybrid', 'Hybrid'

class CarClassification(models.TextChoices):
    NORMAL = 'Normal', 'Normal'
    LUXE = 'Luxe', 'Luxe'
    SPORT = 'Sport', 'Sport'
    UTILITY = 'Utility', 'Utility '

class CarMake(TimestampedModel):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to=upload_make_logo)
    is_top = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class CarModel(TimestampedModel):
    make = models.ForeignKey(CarMake, on_delete=models.PROTECT, related_name="models")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.make.name} {self.name}"

class Car(TimestampedModel):
    car_make = models.ForeignKey(CarMake, on_delete=models.PROTECT, related_name="cars_of_make") 
    car_model = models.ForeignKey(CarModel, on_delete=models.PROTECT, related_name="cars_of_model") 
    car_type = models.CharField(max_length=20, choices=CarType.choices)
    car_class = models.CharField(max_length=10, choices=CarClassification.choices, default=CarClassification.NORMAL)
    
    year = models.CharField(max_length=4, validators=[
        MinLengthValidator(4, message="Year must be exactly 4 characters."),
        RegexValidator(regex=r'^\d{4}$', message='Year must be exactly 4 digits.')
    ], blank=True)
    
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True)
    car_version = models.CharField(max_length=100, blank=True)

    transmission_type = models.CharField(max_length=15, choices=TransmissionType.choices)
    fuel_type = models.CharField(max_length=10, choices=FuelType.choices)
    seats = models.PositiveIntegerField()

    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    month_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    
    max_available_cars = models.PositiveIntegerField(default=0)
    is_unlimited = models.BooleanField(default=False)

    view_count = models.PositiveIntegerField(default=0) 

    is_best = models.BooleanField(default=False)
    is_top_pick = models.BooleanField(default=False)
    is_top_rated = models.BooleanField(default=False)
    is_recently_viewed = models.BooleanField(default=False)
    has_exclusive_offer = models.BooleanField(default=False)

    def get_remaining_cars(self):
        if self.is_unlimited:
            return None
        
        if not self.bookings.exists():
            return self.max_available_cars
        
        now = timezone.now()
        booked_count = self.bookings.filter(
            start_date__lte=now.date(), 
            end_date__gte=now.date()
        ).count()

        return self.max_available_cars - booked_count

    def __str__(self):
        return f"{self.car_make.name} {self.car_model.name} - {self.car_version if self.car_version else ''}"

class CarModelImage(TimestampedModel):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name="car_model_images")
    image = models.ImageField(upload_to=upload_car_image)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.car.car_make.name} {self.car.car_model.name} ({'Main' if self.is_main else 'Additional'})"
