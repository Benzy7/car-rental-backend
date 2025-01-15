from django.db import transaction
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from core.models.car import Car, CarModel
from core.filters.car import CarFilter, CarModelFilter
from core.permissions.is_admin import IsAdminUserRole
from core.permissions.is_not_blacklisted import IsNotBlacklisted
from core.permissions.is_admin_or_owner import IsAdminOrOwner
from core.utils.pagination import CustomPagination  
from core.utils.logger import exception_log
from automobile.serializers.car.read import CarReadSerializer, CarAdminReadSerializer, CarListSerializer, CarByModelListSerializer
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
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'is_archived' in request.data:
            if instance.is_archived and 'is_archived' in request.data and request.data['is_archived'] == False:
                if not request.user.role == 'admin': 
                    raise PermissionDenied("Only admins can unarchive a car.")
            elif request.data['is_archived']:   
                request.data['is_active'] = False
        return super().update(request, *args, **kwargs)

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
        elif self.action in ['create', 'update', 'partial_update', 'destroy', 'admin_retrieve']:
            return [IsAuthenticated(), IsNotBlacklisted(), IsAdminOrOwner()]
        return [IsAuthenticated(), IsNotBlacklisted()] 
    
    def get_queryset(self):
        queryset = Car.objects.filter(is_active=True, is_archived=False)
        return queryset

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

    @action(
        detail=True, 
        methods=['get'], 
        url_path='super', 
    )
    def admin_retrieve(self, request, pk=None):
        try:
            instance = self.get_object()
            if request.user.role != 'admin' and not(
                request.user.role == 'partner' and instance.partner.manager == request.user
            ):
                return Response({"detail": "You do not have permission to access this resource."}, status=status.HTTP_403_FORBIDDEN)
            serializer = CarAdminReadSerializer(instance)
            return Response({"info": "CAR_FETCHED_SUCCESSFULLY", "data": serializer.data}, status=status.HTTP_200_OK)
        except Car.DoesNotExist:
            return Response({"info": "CAR_NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            exception_log(e,__file__)
            return Response({"info": "UNEXPECTED_ERROR_OCCURRED", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False, 
        methods=['get'], 
        url_path='super-list', 
    )
    def admin_list(self, request):
        if request.user.role == 'admin':
            cars = Car.objects.all()
        elif request.user.role == 'partner':
            cars = Car.objects.filter(partner__manager=request.user, is_archived=False)
        else:
            return Response({"detail": "You do not have permission to access this resource."}, status=status.HTTP_403_FORBIDDEN)

        # Paginate the result
        page = self.paginate_queryset(cars)
        if page is not None:
            serializer = CarAdminReadSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        # If no pagination, return all results
        serializer = CarAdminReadSerializer(cars, many=True)
        return Response({"info": "CARS_FETCHED_SUCCESSFULLY", "data": serializer.data}, status=status.HTTP_200_OK)

class CarListByModelAPIView(ListAPIView):
    queryset = CarModel.objects.prefetch_related('cars_of_model')
    pagination_class = CustomPagination  
    serializer_class = CarByModelListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarModelFilter

class ExploreCarsAPIView(APIView):
    permission_classes = []

    def get(self, request):
        try:
            luxe_cars = Car.objects.filter(car_class='luxe')[:3]
            top_cars = Car.objects.filter(is_top_pick=True).exclude(car_class='luxe')[:5]
            popular_cars = Car.objects.filter(is_popular=True).exclude(car_class='luxe')[:10]

            luxe_cars_serializer = CarListSerializer(luxe_cars, many=True)
            top_cars_serializer = CarListSerializer(top_cars, many=True)
            popular_cars_serializer = CarListSerializer(popular_cars, many=True)
            
            response_data = {
                "luxe_cars": luxe_cars_serializer.data,
                "top_cars": top_cars_serializer.data,
                "popular_cars": popular_cars_serializer.data,
            }
            
            return Response({"info": "EXPLORE_CARS_FETCHED_SUCCESSFULLY", "data": response_data}, status=status.HTTP_200_OK)
        except Exception as e:
            exception_log(e,__file__)
            return Response({"info": "UNEXPECTED_ERROR_OCCURRED", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

