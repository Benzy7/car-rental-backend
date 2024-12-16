from .base import TimestampedModel
from django.db import models
from django.utils import timezone
from core.models.user import User
from core.models.partner import Partner

class Coupon(TimestampedModel):
    class CouponType(models.TextChoices):
        DISCOUNT = 'discount', 'Discount'
        FIXED_DISCOUNT = 'fixed_discount', 'Fixed Discount'  
        # FREE_UPGRADE = 'free_upgrade', 'Free Upgrade'
        # FREE_DAY = 'free_day', 'Free Day'
        # WEEKEND_SPECIAL = 'weekend_special', 'Weekend Special'
        # EARLY_BIRD = 'early_bird', 'Early Bird'

    coupon_code = models.CharField(max_length=8, unique=True)
    coupon_type = models.CharField(max_length=50, choices=CouponType.choices, default=CouponType.DISCOUNT)
    coupon_value = models.DecimalField(max_digits=10, decimal_places=2)

    partner = models.ForeignKey(Partner, related_name="partner_coupons", on_delete=models.CASCADE, null=True)
    is_active_for_all_users = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name="user_coupons", on_delete=models.CASCADE, null=True)
    
    expiration_date = models.DateTimeField(null=True, blank=True)
    
    def is_expired(self):
        """Check if the coupon is expired based on expiration date."""
        if self.expiration_date:
            return self.expiration_date < timezone.now()
        return False

    def __str__(self):
        return f"{self.coupon_type} - {self.coupon_value}"

class CouponRedemption(TimestampedModel):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    redeemed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Coupon {self.coupon.coupon_code} redeemed by {self.user} on {self.redeemed_at}"
