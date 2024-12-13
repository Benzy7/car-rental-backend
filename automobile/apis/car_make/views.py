from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from core.models.car import CarMake
from core.utils.logger import exception_log
from core.permissions.is_admin import IsAdminUserRole
from core.permissions.is_not_blacklisted import IsNotBlacklisted
from automobile.serializers.car_make.read import CarMakeReadSerializer, TopCarMakeReadSerializer
from automobile.serializers.car_make.update import CarMakeUpdateSerializer
from automobile.serializers.car_make.create import CarMakeCreateSerializer

class CarMakeViewSet(viewsets.ModelViewSet):
    queryset = CarMake.objects.all()

    def get_serializer_class(self):
        if self.action in ['create']:
            return CarMakeCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CarMakeUpdateSerializer
        return CarMakeReadSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsNotBlacklisted()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsNotBlacklisted(), IsAdminUserRole()]
        return [IsAuthenticated(), IsNotBlacklisted()] 

    @transaction.atomic
    def perform_create(self, serializer):
        name = serializer.validated_data['name']
        if CarMake.objects.filter(name__iexact=name).exists():
            raise ValidationError({'name': ['Car make with this name already exists.']})        
        serializer.save()

    @transaction.atomic
    def perform_update(self, serializer):
        name = serializer.validated_data['name']
        instance = serializer.instance
        if name != instance.name and CarMake.objects.filter(name__iexact=name).exclude(id=instance.id).exists():
            raise ValidationError({'name': ['Car make with this name already exists.']})
        serializer.save()

class TopCarMakesAPIView(APIView):
    permission_classes = [IsAuthenticated, IsNotBlacklisted]

    def get(self, request):
        try:
            top_makes = CarMake.objects.filter(is_top=True).only('name', 'logo')
            serializer = TopCarMakeReadSerializer(top_makes, many=True)
            return Response({"info": "TOP_CAR_MAKES_FETCHED_SUCCESSFULLY", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            exception_log(e,__file__)
            return Response({"info": "UNEXPECTED_ERROR_OCCURRED", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
