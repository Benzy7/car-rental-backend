from rest_framework import serializers
from core.models.car import CarImage

class CarImageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'image', 'is_main']
        read_only_fields = fields
