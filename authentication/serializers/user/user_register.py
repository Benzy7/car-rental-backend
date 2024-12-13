from django.utils import timezone
from rest_framework import serializers
from core.models import User, ReferralCode, ReferralCodeUsage, Parameters, Coupon
from core.models.user import Role
from core.utils.code_generator import generate_coupon_code
    
class ClientRegisterSerializer(serializers.ModelSerializer):
    referral_code = serializers.CharField(max_length=8, required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'referral_code']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        referral_code = validated_data.pop('referral_code', None)
        validated_data['role'] = Role.CLIENT
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        
        if referral_code:
            referral = ReferralCode.objects.filter(referral_code=referral_code, is_active=True).first()
            if referral:
                ReferralCodeUsage.objects.create(referral_code=referral, used_by=user, used_by_email=user.email)
                
                params = Parameters.get_instance()
                
                coupon_code = generate_coupon_code(params.referral_coupon_type, partner_name=referral.partner.name if referral.partner else "")
                expiration_date = timezone.now() + timezone.timedelta(days=params.referral_coupon_expiration_in_days)
                
                Coupon.objects.create(
                    coupon_code=coupon_code,
                    coupon_type=params.referral_coupon_type,
                    coupon_value=params.referral_coupon_value,
                    partner=referral.partner,
                    is_active_for_all_users=False,
                    user=user,
                    expiration_date=expiration_date
                )
            else:
                print(f"Referral code {referral_code} does not exist or is inactive.")
        return user
