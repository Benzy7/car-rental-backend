from rest_framework import serializers
from core.models.partner import Partner

class PartnerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['name', 'description', 'partner_type', 'email', 'phone_number', 'manager', 'country']
