from rest_framework import serializers
from core.models.car import CarImage
    
class CarImageCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['car', 'image', 'is_main']

    def validate(self, data):
        car = data.get('car') or (self.instance.car if self.instance else None)
        if not car:
            raise serializers.ValidationError("Car must be specified.")
        
        if car.images.count() >= 12 and not self.instance:
            raise serializers.ValidationError("You cannot add more than 12 images.")
        
        if data.get('is_main', False):
            car_images = car.images.all()
            for img in car_images:
                if img.is_main and img != self.instance:
                    raise serializers.ValidationError("Only one image can be marked as 'main'.")
        return data
