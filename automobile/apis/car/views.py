from django.db import transaction
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from core.models.car import Car
from core.filters.car import CarFilter
from core.permissions.is_admin import IsAdminUserRole
from core.utils.pagination import CustomPagination  
from core.utils.logger import exception_log
from automobile.serializers.car.read import CarReadSerializer, CarListSerializer
from automobile.serializers.car.create import CarCreateSerializer
from automobile.serializers.car.update import CarUpdateSerializer
from automobile.serializers.car.delete import CarDeleteSerializer

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    pagination_class = CustomPagination  
    filter_backends = [DjangoFilterBackend, OrderingFilter]  
    filterset_class = CarFilter  
    # filterset_fields = ['car_make', 'car_type', 'fuel_type', 'transmission_type', 'seats']
    ordering_fields = ['price_per_day']  
    ordering = ['-created_at']  
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CarListSerializer
        elif self.action == 'create':
            return CarCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return CarUpdateSerializer
        elif self.action == 'destroy':
            return CarDeleteSerializer
        return CarReadSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUserRole()]
        return [IsAuthenticated()] 
    
    def retrieve(self, request, *args, **kwargs):
        car = self.get_object()

        try:
            car.view_count = F('view_count') + 1
            car.save()
        except Exception as e:
            exception_log(e,__file__, 'car view_count')

        serializer = self.get_serializer(car)
        return Response(serializer.data)

    @transaction.atomic
    def perform_destroy(self, instance):
        now = timezone.now().date()
        non_completed_bookings = instance.bookings.filter(
            end_date__gte=now
        )

        if non_completed_bookings.exists():
            raise ValidationError("The car cannot be deleted as it has active or ongoing bookings.")

        instance.delete()
