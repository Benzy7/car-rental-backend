from rest_framework import serializers
from core.models.car import CarModel
from automobile.serializers.car_model_image.read import CarModelImageReadSerializer

class CarModelListSerializer(serializers.ModelSerializer):
    make = serializers.CharField(source='make.name', read_only=True)
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = CarModel
        fields = ['id', 'make', 'name', 'description', 'main_image']
        read_only_fields = fields

    def get_main_image(self, obj):
        main_image = obj.car_model_images.filter(is_main=True).first()
        return main_image.image.url if main_image else None

class CarModelRetrieveSerializer(serializers.ModelSerializer):
    make = serializers.CharField(source='make.name', read_only=True)
    car_model_images = CarModelImageReadSerializer(many=True, read_only=True) 

    class Meta:
        model = CarModel
        fields = ['id', 'make', 'name', 'description', 'car_model_images']
        read_only_fields = fields
    
class CarModelLiteReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarModel
        fields = ['id', 'name']
        read_only_fields = fields
