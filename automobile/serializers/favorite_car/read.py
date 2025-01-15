from rest_framework import serializers
from core.models.car import Car
    
class CarFavoriteListSerializer(serializers.ModelSerializer):
    car_make = serializers.CharField(source='car_make.name', read_only=True)
    car_model = serializers.CharField(source='car_model.name', read_only=True)
    partner_name = serializers.CharField(source='partner.name', read_only=True)
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = [
            'id' ,'partner_name', 'car_make', 'car_model', 'transmission_type', 
            'car_type', 'fuel_type', 'seats', 'price_per_day', 'price_currency',
            'car_variant', 'year', 'main_image', 'is_active',
        ]
        read_only_fields = fields

    def get_main_image(self, obj):
        main_image = obj.car_images.first()
        return main_image.image.url if main_image else None

