from django.db import transaction
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from core.models.car import Car, CarModel
from core.filters.car import CarFilter, CarModelFilter
from core.permissions.is_admin import IsAdminUserRole
from core.permissions.is_not_blacklisted import IsNotBlacklisted
from core.utils.pagination import CustomPagination  
from core.utils.logger import exception_log
from automobile.serializers.car.read import CarReadSerializer, CarListSerializer, CarByModelListSerializer
from automobile.serializers.car.create import CarCreateSerializer
from automobile.serializers.car.update import CarUpdateSerializer
from automobile.serializers.car.delete import CarDeleteSerializer

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    pagination_class = CustomPagination  
    filter_backends = [DjangoFilterBackend, OrderingFilter]  
    filterset_class = CarFilter  
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
            return []
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsNotBlacklisted(), IsAdminUserRole()]
        return [IsAuthenticated(), IsNotBlacklisted()] 
    
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

class CarListByModelAPIView(ListAPIView):
    queryset = CarModel.objects.prefetch_related('cars_of_model')
    pagination_class = CustomPagination  
    serializer_class = CarByModelListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarModelFilter
