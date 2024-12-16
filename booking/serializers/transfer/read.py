from rest_framework import serializers
from core.models import Airport, TransferDestination

class TransferDestinationReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferDestination
        fields = ['id', 'city', 'price']

class AirportReadSerializer(serializers.ModelSerializer):
    transfer_destinations = TransferDestinationReadSerializer(many=True, read_only=True)

    class Meta:
        model = Airport
        fields = ['id', 'name', 'transfer_destinations']
