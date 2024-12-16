from rest_framework import serializers
from core.models.car import Car, CarModel
from automobile.serializers.car_model.read import CarModelRetrieveSerializer
from automobile.serializers.car_images.read import CarModelImageReadSerializer, CarImageReadSerializer

class CarReadSerializer(serializers.ModelSerializer):
    car_model = CarModelRetrieveSerializer(read_only=True)
    remaining_cars = serializers.SerializerMethodField()
    car_images = CarImageReadSerializer(many=True, read_only=True) 

    class Meta:
        model = Car
        fields = [
            'id', 'car_model', 'car_type', 'car_class', 'car_version', 'car_images',
            'transmission_type', 'fuel_type', 'seats', 'price_per_month', 'price_per_day', 
            'is_unlimited', 'max_available_cars', 'year', 'view_count' ,'remaining_cars'
        ]
        read_only_fields = fields

    def get_remaining_cars(self, obj):
        return obj.get_remaining_cars()
    
class CarListSerializer(serializers.ModelSerializer):
    car_make = serializers.CharField(source='car_make.name', read_only=True)
    car_model = serializers.CharField(source='car_model.name', read_only=True)
    partner_name = serializers.CharField(source='partner.name', read_only=True)
    remaining_cars = serializers.SerializerMethodField()
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = [
            'id' ,'partner_name', 'car_make', 'car_model', 'transmission_type', 
            'car_type', 'fuel_type', 'seats', 'price_per_day', 'price_per_month',
            'car_version', 'year', 'remaining_cars', 'main_image',
        ]
        read_only_fields = fields

    def get_remaining_cars(self, obj):
        return obj.get_remaining_cars()

    def get_main_image(self, obj):
        main_image = obj.car_images.filter(is_main=True).first()
        return main_image.image.url if main_image else None

class CarByModelListSerializer(serializers.ModelSerializer):
    cars = CarListSerializer(many=True, source='cars_of_model')
    car_model_images = CarModelImageReadSerializer(many=True, read_only=True) 
    make = serializers.CharField(source='make.name', read_only=True)
    model = serializers.CharField(source='name', read_only=True)

    class Meta:
        model = CarModel
        fields = ['make', 'model', 'description', 'cars', 'car_model_images']
