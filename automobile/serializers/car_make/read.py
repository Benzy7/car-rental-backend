from rest_framework import serializers
from core.models.car import CarMake

class CarMakeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMake
        fields = ['id', 'name', 'logo', 'is_top']
        read_only_fields = fields

class TopCarMakeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMake
        fields = ['id', 'name', 'logo']
        read_only_fields = fields

class CarMakeLiteReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMake
        fields = ['id', 'name']
        read_only_fields = fields