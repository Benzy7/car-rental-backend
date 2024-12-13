from rest_framework import serializers
from core.models.car import CarModelImage

class CarModelImageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModelImage
        fields = ['id', 'image', 'is_main']
        read_only_fields = fields
