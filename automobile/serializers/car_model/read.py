from rest_framework import serializers
from core.models.car import CarModel
from automobile.serializers.car_make.read import CarMakeReadSerializer

class CarModelReadSerializer(serializers.ModelSerializer):
    make = CarMakeReadSerializer(read_only=True) 

    class Meta:
        model = CarModel
        fields = ['id', 'make', 'name']
        read_only_fields = fields

class CarModelLiteReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarModel
        fields = ['id', 'name']
        read_only_fields = fields
