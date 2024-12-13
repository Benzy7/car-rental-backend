from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from core.permissions.is_admin import IsAdminUserRole
from core.permissions.is_not_blacklisted import IsNotBlacklisted
from core.models.car import CarModelImage
from automobile.serializers.car_model_image.create_or_update import CarModelImageCreateUpdateSerializer
from automobile.serializers.car_model_image.delete import CarModelImageDeleteSerializer

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