from rest_framework import serializers

class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    pin_code = serializers.CharField(min_length=6, max_length=6)
    new_password = serializers.CharField(min_length=8)