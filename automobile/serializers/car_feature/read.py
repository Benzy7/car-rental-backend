from rest_framework import serializers
from core.models.car_feature import CarFeature

class CarFeatureListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarFeature
        fields = ['id', 'name', 'price', 'is_active']
        read_only_fields = fields

class CarFeatureRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarFeature
        fields = ['id', 'name', 'description', 'price', 'is_active']
        read_only_fields = fields

class BookCarFeatureReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarFeature
        fields = ['id', 'name', 'price']
        read_only_fields = fields
