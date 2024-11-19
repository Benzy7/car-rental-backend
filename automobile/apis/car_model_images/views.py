from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from core.models.car import CarImage
from core.permissions.is_admin import IsAdminUserRole
from automobile.serializers.car_model_image.create_or_update import CarImageCreateUpdateSerializer
from automobile.serializers.car_model_image.delete import CarImageDeleteSerializer

class CarImageViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = CarImage.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CarImageCreateUpdateSerializer
        if self.action == 'destroy':
            return CarImageDeleteSerializer
        return super().get_serializer_class()