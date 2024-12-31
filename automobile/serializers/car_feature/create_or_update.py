# car/serializers.py
from rest_framework import serializers
from core.models.car_feature import CarFeature

class CarFeatureCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarFeature
        fields = ['name', 'description', 'price', 'is_active']
