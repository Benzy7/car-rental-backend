from rest_framework import serializers
from core.models.car import Car

class CarDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id']
