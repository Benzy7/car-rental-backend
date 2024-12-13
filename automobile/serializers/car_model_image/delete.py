from rest_framework import serializers
from core.models.car import CarModelImage

class CarModelImageDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModelImage
        fields = ['id']

    def validate(self, attrs):
        instance = self.instance
        if instance.is_main:
            raise serializers.ValidationError("Cannot delete the main image directly. Set another image as main first.")
        return attrs