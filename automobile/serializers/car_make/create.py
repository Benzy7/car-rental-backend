from rest_framework import serializers
from core.models.car import CarMake

class CarMakeCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CarMake
        fields = ['name', 'logo', 'is_top']
