from rest_framework import serializers
from core.models.car import Car, CarModel
from automobile.serializers.car_make.read import CarMakeLiteReadSerializer
from automobile.serializers.car_model.read import CarModelLiteReadSerializer

class CarReadSerializer(serializers.ModelSerializer):
    car_make = CarMakeLiteReadSerializer(read_only=True)
    car_model = CarModelLiteReadSerializer(read_only=True)
    remaining_cars = serializers.SerializerMethodField()
    
    class Meta:
        model = Car
        fields = [
            'id', 'car_make', 'car_model', 'car_type', 'car_class', 'car_version', 
            'description', 'transmission_type', 'fuel_type', 'seats',
            'month_price', 'price_per_day', 'is_unlimited', 'max_available_cars',
            'year', 'view_count' ,'remaining_cars', 
        ]
        read_only_fields = fields

    def get_remaining_cars(self, obj):
        return obj.get_remaining_cars()
    
class CarListSerializer(serializers.ModelSerializer):
    car_make = serializers.CharField(source='car_make.name', read_only=True)
    car_model = serializers.CharField(source='car_model.name', read_only=True)
    partner_name = serializers.CharField(source='partner.name', read_only=True)
    remaining_cars = serializers.SerializerMethodField()
    
    class Meta:
        model = Car
        fields = [
            'id' ,'partner_name', 'car_make', 'car_model', 'transmission_type', 
            'car_type', 'fuel_type', 'seats', 'price_per_day', 'month_price',
            'car_version', 'year', 'remaining_cars',
        ]
        read_only_fields = fields

    def get_remaining_cars(self, obj):
        return obj.get_remaining_cars()

class CarByModelListSerializer(serializers.ModelSerializer):
    cars = CarListSerializer(many=True, source='cars_of_model')
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = CarModel
        fields = ['name', 'description', 'main_image', 'cars']
        
    def get_main_image(self, obj):
        main_image = obj.car_model_images.filter(is_main=True).first()
        return main_image.image.url if main_image else None
