from django.db import transaction
from django.db.models import Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from core.permissions.is_not_blacklisted import IsNotBlacklisted
from core.utils.logger import exception_log
from core.models import FavoriteCar, Car, CarImage
from automobile.serializers.favorite_car.read import CarFavoriteListSerializer

class FavoriteCarView(APIView):
    permission_classes = [IsAuthenticated, IsNotBlacklisted]
    
    @transaction.atomic
    def post(self, request):
        try:
            user = request.user
            car_id = request.data.get('car_id')
            if not car_id:
                return Response({"info": "VALIDATION_ERROR", "details": "'car_id' is required."}, status=status.HTTP_400_BAD_REQUEST)

            car = Car.objects.only('id').get(id=car_id)
            _favorite, created = FavoriteCar.objects.get_or_create(user=user, car=car)
            if created:
                return Response({"info": "CAR_ADDED_TO_FAVORITES"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"info": "CAR_IS_ALREADY_IN_FAVORITES"}, status=status.HTTP_200_OK)
        except Car.DoesNotExist:
            return Response({"info": "CAR_NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            exception_log(e,__file__)
            transaction.set_rollback(True)
            return Response({"info": "UNEXPECTED_ERROR_OCCURRED", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def delete(self, request):
        try:
            user = request.user
            car_id = request.data.get('car_id')
            if not car_id:
                return Response({"info": "VALIDATION_ERROR", "details": "'car_id' is required."}, status=status.HTTP_400_BAD_REQUEST)

            car = Car.objects.only('id').get(id=car_id)
            favorite = FavoriteCar.objects.get(user=user, car=car)
            favorite.delete()
            return Response({"info": "CAR_REMOVED_FROM_FAVORITES"}, status=status.HTTP_200_OK)
        except Car.DoesNotExist:
            transaction.set_rollback(True)
            return Response({"info": "CAR_NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)
        except FavoriteCar.DoesNotExist:
            transaction.set_rollback(True)
            return Response({"info": "CAR_NOT_FOUND_IN_FAVORITES"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            exception_log(e,__file__)
            transaction.set_rollback(True)
            return Response({"info": "UNEXPECTED_ERROR_OCCURRED", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            user = request.user
            favorite_cars = Car.objects.filter(favorited_by__user=user).select_related('partner', 'car_make', 'car_model').prefetch_related(
                Prefetch('car_images', queryset=CarImage.objects.filter(is_main=True))
            ).only(
                'id' ,'partner', 'car_make', 'car_model', 'transmission_type', 
                'car_type', 'fuel_type', 'seats', 'price_per_day', 'price_currency',
                'car_variant', 'year', 'is_active',
            )
            if not favorite_cars.exists():
                return Response({"info": "NO_FAVORITES_FOUND", "details": "You don't have any favorite cars yet."}, status=status.HTTP_200_OK)
            serializer = CarFavoriteListSerializer(favorite_cars, many=True)
            return Response({"info": "FAVORITES_RETRIEVED_SUCCESSFULLY", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            exception_log(e,__file__)
            return Response({"info": "UNEXPECTED_ERROR_OCCURRED", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
