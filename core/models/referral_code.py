from django.db import models
from core.models.user import User
from core.models.base import TimestampedModel

class ReferralCode(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    user_email = models.EmailField()
    referral_code = models.CharField(max_length=8, unique=True)
    usage_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Referral code for {self.user.email}: {self.referral_code}"

class ReferralCodeUsage(TimestampedModel):
    referral_code = models.ForeignKey(ReferralCode, on_delete=models.CASCADE, null=True)
    used_by = models.ForeignKey(User, related_name='used_referral_codes', on_delete=models.SET_NULL, null=True)
    used_by_email = models.EmailField()  
    is_claimed = models.BooleanField(default=False)
    def __str__(self):
        return f"Referral Code {self.referral_code.code} used by {self.used_by.username} at {self.created_at}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.referral_code.usage_count += 1
            self.referral_code.save(update_fields=['usage_count'])

        super().save(*args, **kwargs)

class ReferralCodeReward(TimestampedModel):
    referral_usage = models.ForeignKey(ReferralCodeUsage, on_delete=models.CASCADE, related_name='rewards')
    reward_type = models.CharField(max_length=100)
    reward_value = models.DecimalField(max_digits=10, decimal_places=2)
    is_redeemed = models.BooleanField(default=False)
    redeemed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Reward for {self.referral_usage.referral_code.user} - {self.reward_type}"
    