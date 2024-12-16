from rest_framework import serializers
from core.models.car import CarModelImage, CarImage

class CarModelImageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModelImage
        fields = ['id', 'image', 'is_main']
        read_only_fields = fields

class CarImageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'image', 'is_main']
        read_only_fields = fields
