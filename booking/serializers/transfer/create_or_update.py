from rest_framework import serializers
from core.models import Airport, TransferDestination

class AirportCreateOrUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airport
        fields = ['id', 'name']

class TransferDestinationCreateOrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferDestination
        fields = ['id', 'airport', 'city', 'price']
