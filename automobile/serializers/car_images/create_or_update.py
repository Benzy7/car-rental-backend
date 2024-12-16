from rest_framework import serializers
from core.models.car import CarModelImage, CarImage
    
class CarModelImageCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModelImage
        fields = ['car_model', 'image', 'is_main']

    def validate(self, data):
        car_model = data.get('car_model') or (self.instance.car_model if self.instance else None)
        if not car_model:
            raise serializers.ValidationError("Car model must be specified.")
        
        if car_model.car_model_images.count() >= 5 and not self.instance:
            raise serializers.ValidationError("You cannot add more than 5 images.")
        
        if data.get('is_main', False):
            car_images = car_model.car_model_images.all()
            for img in car_images:
                if img.is_main and img != self.instance:
                    raise serializers.ValidationError("Only one image can be marked as 'main'.")
        return data

class CarImageCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['car', 'image', 'is_main']

    def validate(self, data):
        car = data.get('car') or (self.instance.car if self.instance else None)
        if not car:
            raise serializers.ValidationError("Car must be specified.")
        
        if car.car_images.count() >= 12 and not self.instance:
            raise serializers.ValidationError("You cannot add more than 12 images.")
        
        if data.get('is_main', False):
            images = car.car_images.all()
            for img in images:
                if img.is_main and img != self.instance:
                    raise serializers.ValidationError("Only one image can be marked as 'main'.")
        return data
