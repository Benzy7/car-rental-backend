from rest_framework import serializers
from core.models.user import User

class UserProfileSerializer(serializers.ModelSerializer):
    partner_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'country', 'gender', 'role', 'partner_id', 'created_at']
        read_only_fields = fields
        
    def get_partner_id(self, obj):
        partner = obj.partner_set.values('id').first()
        return partner['id'] if partner else None
