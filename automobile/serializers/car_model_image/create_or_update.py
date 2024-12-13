from rest_framework import serializers
from core.models.car import CarModelImage
    
class CarModelImageCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModelImage
        fields = ['car_model', 'image', 'is_main']

    def validate(self, data):
        car_model = data.get('car_model') or (self.instance.car_model if self.instance else None)
        if not car_model:
            raise serializers.ValidationError("Car model must be specified.")
        
        if car_model.car_model_images.count() >= 12 and not self.instance:
            raise serializers.ValidationError("You cannot add more than 12 images.")
        
        if data.get('is_main', False):
            car_images = car_model.car_model_images.all()
            for img in car_images:
                if img.is_main and img != self.instance:
                    raise serializers.ValidationError("Only one image can be marked as 'main'.")
        return data
