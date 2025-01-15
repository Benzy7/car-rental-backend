from rest_framework import serializers
from core.models.partner import Partner

class PartnerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['name', 'description', 'email', 'phone_number']

#TODO: partner country, type and maneger can be chanegd only with admin (actions)
