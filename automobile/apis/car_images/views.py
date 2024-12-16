from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from core.permissions.is_admin import IsAdminUserRole
from core.permissions.is_not_blacklisted import IsNotBlacklisted
from core.models.car import CarModelImage, CarImage
from automobile.serializers.car_images.create_or_update import CarModelImageCreateUpdateSerializer, CarImageCreateUpdateSerializer
from automobile.serializers.car_images.delete import CarModelImageDeleteSerializer, CarImageDeleteSerializer

class CarModelImageViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = CarModelImage.objects.all()
    permission_classes = [IsAuthenticated, IsNotBlacklisted, IsAdminUserRole]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CarModelImageCreateUpdateSerializer
        if self.action == 'destroy':
            return CarModelImageDeleteSerializer
        return super().get_serializer_class()
    
class CarImageViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = CarImage.objects.all()
    permission_classes = [IsAuthenticated, IsNotBlacklisted, IsAdminUserRole]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CarImageCreateUpdateSerializer
        if self.action == 'destroy':
            return CarImageDeleteSerializer
        return super().get_serializer_class()
