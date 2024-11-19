from rest_framework import serializers
from core.models.user import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'gender', 'role', 'created_at']
        read_only_fields = fields
