from rest_framework import serializers
from core.models.car import Car, CarMake, CarModel

class CarCreateSerializer(serializers.ModelSerializer):
    car_make = serializers.PrimaryKeyRelatedField(queryset=CarMake.objects.all())
    car_model = serializers.PrimaryKeyRelatedField(queryset=CarModel.objects.all())
    
    class Meta:
        model = Car
        fields = [
            'car_make', 'car_model', 'car_type', 'car_class', 'car_variant', 
            'seats', 'transmission_type', 'fuel_type', 'year', 'country',
            'price_per_month', 'price_per_day', 'year', 'is_active', 'max_available_cars'
        ]
