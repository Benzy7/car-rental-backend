from django.utils import timezone
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from core.models import Airport, TransferDestination
from core.permissions.is_admin import IsAdminUserRole
from core.permissions.is_not_blacklisted import IsNotBlacklisted
from core.utils.logger import exception_log
from .transfer_data import data
from booking.serializers.transfer.create_or_update import AirportCreateOrUpdateSerializer, TransferDestinationCreateOrUpdateSerializer
from booking.serializers.transfer.read import AirportReadSerializer, TransferDestinationReadSerializer

class GenerateAirportTransferDataView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserRole]
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            for airport_name, destinations in data.items():
                airport, _created = Airport.objects.get_or_create(name=airport_name)
                for city, price in destinations.items():
                    TransferDestination.objects.get_or_create(airport=airport, city=city, price=price)

            return Response({"info": "DATA_GENERATED_SUCCESSFULLY"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            exception_log(e,__file__)
            transaction.set_rollback(True)
            return Response({"info": "UNEXPECTED_ERROR_OCCURRED", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return AirportCreateOrUpdateSerializer
        elif self.action == 'partial_update':
            return None
        return AirportReadSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsNotBlacklisted(), IsAdminUserRole()]
        return [IsAuthenticated(), IsNotBlacklisted()] 

class TransferDestinationViewSet(viewsets.ModelViewSet):
    queryset = TransferDestination.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return TransferDestinationCreateOrUpdateSerializer
        elif self.action == 'partial_update':
            return None
        return TransferDestinationReadSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsNotBlacklisted(), IsAdminUserRole()]
        return [IsAuthenticated(), IsNotBlacklisted()] 
