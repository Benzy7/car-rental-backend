from rest_framework import serializers
from core.models.partner import Partner

class PartnerDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['id']
