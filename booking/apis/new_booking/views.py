from django.utils import timezone
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from core.utils.logger import exception_log
from booking.serializers.booking.create import NewBookingSerializer
from core.permissions.is_not_blacklisted import IsNotBlacklisted
from core.models import CarBooking, Car, Coupon, CouponRedemption, User, Airport, TransferDestination, Parameters, \
    CarFeature, BookingFeature

class NewBookingView(APIView):
    serializer_class = NewBookingSerializer
    permission_classes = [IsAuthenticated, IsNotBlacklisted]
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response({"info": "VALIDATION_ERROR", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            # Extract the data
            validated_data = serializer.validated_data
            car_id = validated_data.get('car_id')
            feature_ids = validated_data.get('features', [])
            coupon_code = validated_data.get('coupon_id', '')
            user_id = validated_data.get('user_id')
            start_date = validated_data.get('start_date')
            end_date = validated_data.get('end_date')
            pickup_time = validated_data.get('pickup_time')
            return_time = validated_data.get('return_time')
            booking_type = validated_data.get('booking_type')
            with_driver = validated_data.get('with_driver', False)
            additional_notes = validated_data.get('additional_notes', '')
            phone_number_1 = validated_data.get('phone_number_1', '')
            phone_number_2 = validated_data.get('phone_number_2', '')
            flight_number = validated_data.get('flight_number', '')
            plane_arrival_datetime = validated_data.get('plane_arrival_datetime', None)
            airport_id = validated_data.get('airport_id', None)
            transfer_destination_id = validated_data.get('transfer_destination_id', None)

            if start_date < timezone.now().date():
                return Response({"info": "START_DATE_ERROR", "details": "Start date must be in the future."}, status=status.HTTP_400_BAD_REQUEST)

            if end_date <= start_date:
                return Response({"info": "END_DATE_ERROR", "details": "End date must be after the start date."}, status=status.HTTP_400_BAD_REQUEST)

            if booking_type not in ('standard', 'event', 'transfer',):
                return Response({"info": "INVALID_BOOKING_TYPE"}, status=status.HTTP_400_BAD_REQUEST)

            nb_booking_days = (end_date - start_date).days
            if booking_type == "standard" and nb_booking_days < 3:
                return Response({
                    "info": "BOOKING_LENGTH_ERROR", 
                    "details": "Standard bookings must be for at least 3 days."
                }, status=status.HTTP_400_BAD_REQUEST)
            elif (booking_type == "event" or booking_type == "transfer") and nb_booking_days != 1:
                return Response({
                    "info": "BOOKING_LENGTH_ERROR", 
                    "details": "Tranfer and Event bookings must be for one day only."
                }, status=status.HTTP_400_BAD_REQUEST)

            airport = None
            transfer_destination = None
            if booking_type == "event" or booking_type == "transfer":
                with_driver = True
                if booking_type == "transfer": 
                    if not(flight_number and plane_arrival_datetime and airport_id and transfer_destination_id):
                        return Response({
                            "info": "VALIDATION_ERROR", 
                            "details": "The airport, destination, flight number and plane arrival date fields are required for transfer bookings."
                        }, status=status.HTTP_400_BAD_REQUEST)
                    airport = Airport.objects.get(id=airport_id).only('id', 'name')
                    transfer_destination = TransferDestination.objects.filter(id=transfer_destination, airport=airport).only('city', 'price')
                    
            # 1. Validate Car
            user = User.objects.filter(pk=user_id).only('id', 'email').first()
            if not user:
                return Response({"info": "USER_NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)
            #TODO: check car availblity
            car = Car.objects.filter(pk=car_id).only(
                'id', 'price_per_day', 'price_per_month', 'car_make__name', 'car_model__name', 'car_version'
            ).first()
            if not car:
                return Response({"info": "CAR_NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)
                
            # 2. Validate Coupon
            #TODO: add other types
            coupon = None
            if coupon_code:
                try:
                    coupon = Coupon.objects.filter(coupon_code=coupon_code).only('user__id', 'is_active_for_all_users').first()
                    if not(coupon.user == user or coupon.is_active_for_all_users):
                        return Response({"info": "COUPON_INVALID"}, status=status.HTTP_400_BAD_REQUEST)
                    if coupon.is_expired:
                        return Response({"info": "COUPON_EXPIRED"}, status=status.HTTP_400_BAD_REQUEST)
                    if CouponRedemption.objects.filter(coupon=coupon, user=user).exists():
                        return Response({"info": "COUPON_ALREADY_REDEEMED"}, status=status.HTTP_400_BAD_REQUEST)
                except Coupon.DoesNotExist:
                    return Response({"info": "COUPON_NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)

            # Features calculation
            features_fee = 0.0
            if feature_ids:
                features = CarFeature.objects.filter(id__in=feature_ids).only('name', 'price', 'is_active')
                if len(features) != len(feature_ids):
                    return Response({
                        "info": "FEATURE_NOT_FOUND", 
                        "details": "One or more feature were not found."
                        }, status=status.HTTP_404_NOT_FOUND)
                for feature in features:
                    if not feature.is_active:
                        return Response({
                            "info": "FEATURE_UNAVAILABLE", 
                            "details": f"{feature.name} is currently unavailable."
                        }, status=status.HTTP_400_BAD_REQUEST)
                    BookingFeature.objects.create(booking=booking, feature=feature, price=feature.price)
                    features_fee += feature.price

            # Base price calculation
            base_price = (float(car.price_per_day)  * nb_booking_days) + features_fee
            params = Parameters.get_instance(
                fields=['driver_price_perday', 'long_duration_discount', 'medium_duration_discount', 'short_duration_discount']
            )
            transfer_fee = 0.0
            driver_fee = 0.0
            if booking_type == "transfer": 
                transfer_fee = float(transfer_destination.price)
                base_price += transfer_fee
            if with_driver:
                driver_fee = float(params.driver_price_perday) * nb_booking_days
                base_price += driver_fee
            

            # Standard discount calculation
            # discount = 0.0
            # monthly_price = None
            if nb_booking_days >= 30:
                # if car.price_per_month:
                #     nb_months = nb_booking_days // 30
                #     remaining_days = nb_booking_days % 30
                #     monthly_price = float(car.price_per_month) * nb_months + float(car.price_per_day) * remaining_days
                # else:
                discount = float(params.long_duration_discount)
            elif nb_booking_days >= 14:
                discount = float(params.medium_duration_discount)
            elif nb_booking_days >= 7:
                discount = float(params.short_duration_discount)
            
            # if monthly_price and (base_price > monthly_price):
            #     normal_discount = base_price - monthly_price
            # else:
            normal_discount = base_price * discount
            
            # Coupon discount calculation
            coupon_discount = 0.0
            if coupon:
                if coupon.coupon_type == "discount":
                    coupon_discount = base_price * (coupon.coupon_value / 100)
                elif coupon.coupon_type == "fixed_discount":
                    coupon_discount = coupon.coupon_value
                CouponRedemption.objects.create(coupon=coupon, user=user)

            # Final cost calculation
            total_cost = base_price - normal_discount - coupon_discount
            
            booking = {}
            booking['car'] = car
            booking['user'] = user
            booking['car_description'] = f"{car.car_make.name} {car.car_model.name} {car.car_version}"
            booking['user_email'] = user.email
            booking['booking_type'] = booking_type
            booking['status'] = "pending"
            booking['start_date'] = start_date
            booking['end_date'] = end_date
            booking['pickup_time'] = pickup_time
            booking['return_time'] = return_time
            booking['with_driver'] = with_driver
            booking['additional_notes'] = additional_notes
            booking['phone_number_1'] = phone_number_1
            booking['phone_number_2'] = phone_number_2
            booking['flight_number'] = flight_number
            booking['plane_arrival_datetime'] = plane_arrival_datetime
            booking['airport'] = airport
            booking['transfer_destination'] = transfer_destination
            booking['transfer_description'] =  f"{airport.name if airport else 'airport'} -> {transfer_destination.city if transfer_destination else 'destination'}" if booking_type == "transfer" else ""
            booking['coupon'] = coupon
            booking['coupon_code'] = coupon_code
            booking['driver_fee'] = driver_fee     
            booking['features_fee'] = features_fee     
            booking['transfer_fee'] = transfer_fee                   
            booking['normal_discount'] = normal_discount
            booking['coupon_discount'] = coupon_discount
            booking['total_discount'] = normal_discount + coupon_discount
            booking['total_cost'] = base_price
            booking['final_total_cost'] = total_cost
            CarBooking.objects.create(**booking)

            return Response({"info": "NEW_BOOKING_CREATED_SUCCESSFULLY"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            exception_log(e,__file__)
            transaction.set_rollback(True)
            return Response({"info": "UNEXPECTED_ERROR_OCCURRED", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
