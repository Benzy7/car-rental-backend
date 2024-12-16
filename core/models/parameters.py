from django.db import models
from .base import TimestampedModel

class Parameters(TimestampedModel):
    profile_picture_size = models.IntegerField(default=5)
    
    referral_coupon_type = models.CharField(max_length=50, default="discount")
    referral_coupon_expiration_in_days = models.IntegerField(default=15)
    referral_coupon_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    driver_price_perday = models.DecimalField(max_digits=10, decimal_places=2, default=50.0)
    
    long_duration_discount = models.DecimalField(max_digits=4, decimal_places=2, default=0.1)  # 10%
    medium_duration_discount = models.DecimalField(max_digits=4, decimal_places=2, default=0.05)  # 5%
    short_duration_discount = models.DecimalField(max_digits=4, decimal_places=2, default=0.02)  # 2%
    
    @classmethod
    def get_instance(cls):
        instance, _created = cls.objects.get_or_create(id=1)
        return instance
