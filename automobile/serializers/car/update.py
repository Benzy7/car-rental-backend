from rest_framework import serializers
from core.models.car import Car, CarMake, CarModel

class CarUpdateSerializer(serializers.ModelSerializer):
    car_make = serializers.PrimaryKeyRelatedField(queryset=CarMake.objects.all())
    car_model = serializers.PrimaryKeyRelatedField(queryset=CarModel.objects.all())

    class Meta:
        model = Car
        fields = [
            'car_make', 'car_model', 'car_type', 'car_class', 'title', 
            'sub_title', 'description', 'transmission_type', 'fuel_type', 
            'seats', 'price_per_day', 'is_unlimited', 'max_available_cars',
            'is_best', 'is_top_pick', 'is_top_rated', 'is_recently_viewed', 
            'has_exclusive_offer'
        ]
