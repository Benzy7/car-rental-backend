from rest_framework import serializers

class UserRefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
