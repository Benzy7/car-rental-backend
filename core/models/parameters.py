from django.db import models

class Parameters(models.Model):
    profile_picture_size = models.IntegerField(default=5)
    
    referral_coupon_type = models.CharField(max_length=50, default="discount")
    referral_coupon_expiration_in_days = models.IntegerField(default=15)
    referral_coupon_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    transfer_pricing = models.JSONField(default=dict, blank=True)

    @classmethod
    def get_instance(cls):
        instance, _created = cls.objects.get_or_create(id=1)
        return instance
