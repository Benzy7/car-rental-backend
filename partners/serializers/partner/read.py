from rest_framework import serializers
from core.models.partner import Partner

class PartnerReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['id', 'name', 'partner_type', 'email', 'phone_number']
        read_only_fields = fields
