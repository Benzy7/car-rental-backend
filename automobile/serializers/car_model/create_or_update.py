# car/serializers.py
from rest_framework import serializers
from core.models.car import CarModel

class CarModelCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['make', 'name']
