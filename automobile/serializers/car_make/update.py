from rest_framework import serializers
from core.models.car import CarMake

class CarMakeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMake
        fields = ['name', 'logo', 'is_top']
        extra_kwargs = {'logo': {'required': False}}
