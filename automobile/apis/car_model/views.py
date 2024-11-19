from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models.car import CarModel
from core.permissions.is_admin import IsAdminUserRole
from automobile.serializers.car_model.create_or_update import CarModelCreateUpdateSerializer
from automobile.serializers.car_model.read import CarModelReadSerializer


class CarModelViewSet(viewsets.ModelViewSet):
    queryset = CarModel.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CarModelReadSerializer
        return CarModelCreateUpdateSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUserRole()]
        return [IsAuthenticated()] 
