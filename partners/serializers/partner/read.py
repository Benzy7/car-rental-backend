from rest_framework import serializers
from core.models.partner import Partner

class PartnerReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['id', 'name', 'partner_type', 'email', 'phone_number', 'country']
        read_only_fields = fields

class PartnerLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['id', 'name']
        read_only_fields = fields
