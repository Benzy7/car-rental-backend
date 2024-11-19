from rest_framework import serializers
from core.models.car import Car
from automobile.serializers.car_make.read import CarMakeLiteReadSerializer
from automobile.serializers.car_model.read import CarModelLiteReadSerializer
from automobile.serializers.car_model_image.read import CarImageReadSerializer

class CarReadSerializer(serializers.ModelSerializer):
    car_make = CarMakeLiteReadSerializer(read_only=True)
    car_model = CarModelLiteReadSerializer(read_only=True)
    remaining_cars = serializers.SerializerMethodField()
    images = CarImageReadSerializer(many=True, read_only=True) 
    
    class Meta:
        model = Car
        fields = [
            'id', 'car_make', 'car_model', 'car_type', 'car_class', 'title', 
            'sub_title', 'description', 'transmission_type', 'fuel_type', 
            'seats', 'price_per_day', 'is_unlimited', 'max_available_cars',
            'view_count' ,'remaining_cars', 'images'
        ]
        read_only_fields = fields

    def get_remaining_cars(self, obj):
        return obj.get_remaining_cars()
    
class CarListSerializer(serializers.ModelSerializer):
    car_make = serializers.CharField(source='car_make.name', read_only=True)
    car_model = serializers.CharField(source='car_model.name', read_only=True)
    remaining_cars = serializers.SerializerMethodField()
    main_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Car
        fields = [
            'id', 'title' ,'car_make', 'car_model', 'title', 'transmission_type', 
            'car_type', 'fuel_type', 'seats', 'price_per_day', 'remaining_cars',
            'main_image' 
        ]
        read_only_fields = fields

    def get_remaining_cars(self, obj):
        return obj.get_remaining_cars()
    
    def get_main_image(self, obj):
        main_image = obj.images.filter(is_main=True).first()
        return main_image.image.url if main_image else None
