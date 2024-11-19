from rest_framework import serializers
from core.models import User, ReferralCode, ReferralCodeUsage
    
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
        validated_data['role'] = User.CLIENT
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        
        if referral_code:
            referral = ReferralCode.objects.filter(referral_code=referral_code, is_active=True).first()
            if referral:
                ReferralCodeUsage.objects.create(referral_code=referral, used_by=user, used_by_email=user.email)
            else:
                print(f"Referral code {referral_code} does not exist or is inactive.")
        return user
