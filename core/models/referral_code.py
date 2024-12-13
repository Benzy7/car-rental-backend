from django.db import models
from core.models.base import TimestampedModel
from core.models.user import User
from core.models.partner import Partner

class ReferralCode(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    user_email = models.EmailField()
    partner = models.ForeignKey(Partner, on_delete=models.SET_NULL, null=True)
    partner_name = models.CharField(max_length=255, blank=True)
    referral_code = models.CharField(max_length=8, unique=True)
    usage_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.referral_code

class ReferralCodeUsage(TimestampedModel):
    referral_code = models.ForeignKey(ReferralCode, on_delete=models.CASCADE, null=True)
    used_by = models.ForeignKey(User, related_name='used_referral_codes', on_delete=models.SET_NULL, null=True)
    used_by_email = models.EmailField()  

    def __str__(self):
        return f"Referral Code {self.referral_code.referral_code} used by {self.used_by.email} at {self.created_at}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.referral_code.usage_count += 1
            self.referral_code.save(update_fields=['usage_count'])

        super().save(*args, **kwargs)
