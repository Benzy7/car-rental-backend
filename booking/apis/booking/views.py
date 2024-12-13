from django.utils import timezone
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from booking.serializers.booking.create import NewBookingSerializer
from core.models import CarBooking, Car, Coupon, User
from core.utils.logger import exception_log


class NewBookingView(APIView):
    serializer_class = NewBookingSerializer
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response({"info": "VALIDATION_ERROR", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            # Extract the data
            validated_data = serializer.validated_data
            car_id = validated_data.get('car_id')
            coupon_code = validated_data.get('coupon_id', '')
            user_id = validated_data.get('user_id')
            start_date = validated_data.get('start_date')
            end_date = validated_data.get('end_date')
            pickup_date = validated_data.get('pickup_date')
            pickup_time = validated_data.get('pickup_time')
            booking_type = validated_data.get('booking_type')
            with_driver = validated_data.get('with_driver', False)
            additional_notes = validated_data.get('additional_notes', '')

            if start_date < timezone.now().date():
                return Response({"info": "START_DATE_ERROR", "details": "Start date must be in the future."}, status=status.HTTP_400_BAD_REQUEST)

            if end_date <= start_date:
                return Response({"info": "END_DATE_ERROR", "details": "End date must be after the start date."}, status=status.HTTP_400_BAD_REQUEST)

            #TODO: check type
            if booking_type == "standard" and (end_date - start_date).days < 3:
                return Response({"info": "BOOKING_LENGTH_ERROR", "details": "Standard bookings must be for at least 3 days."}, status=status.HTTP_400_BAD_REQUEST)
            elif (booking_type == "event" or booking_type == "transfer") and (end_date - start_date).days != 1:
                return Response({"info": "BOOKING_LENGTH_ERROR", "details": "Event bookings must be for one day only."}, status=status.HTTP_400_BAD_REQUEST)

            # 1. Validate Car
            try:
                #TODO: check car availblity
                user = User.objects.get(pk=user_id)#.only()
                car = Car.objects.get(pk=car_id)#.only()
            except Car.DoesNotExist:
                return Response({"info": "CAR_NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)

            # 2. Validate Coupon
            #TODO: add other types and redmption
            coupon = None
            if coupon_code:
                try:
                    coupon = Coupon.objects.filter(coupon_code=coupon_code).only('user', 'is_active_for_all_users').first()
                    if not(coupon.user == user or coupon.is_active_for_all_users):
                        return Response({"info": "COUPON_INVALID"}, status=status.HTTP_400_BAD_REQUEST)
                    if coupon.is_expired:
                        return Response({"info": "COUPON_EXPIRED"}, status=status.HTTP_400_BAD_REQUEST)
                except Coupon.DoesNotExist:
                    return Response({"info": "COUPON_NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)

            booking_days = (end_date - start_date).days
            #TODO: handle transfert
            if booking_type == "event" or booking_type == "transfer":
                with_driver = True
        
            # Base price calculation
            base_price = float(car.price_per_day)  * booking_days
            driver_fee = 0.0
            if with_driver:
                #TODO: add to params
                driver_fee = 50 * booking_days
                base_price += driver_fee
            
            #TODO: add to params
            # Long-duration discount
            if booking_days >= 30:
                #if price per month
                discount = 0.1  # 10%
            elif booking_days >= 14:
                discount = 0.05  # 5%
            elif booking_days >= 7:
                discount = 0.02  # 2%
            else:
                discount = 0.0
            
            normal_discount = base_price * discount
            
            # Apply coupon
            coupon_discount = 0.0
            if coupon:
                if coupon.coupon_type == "discount":
                    coupon_discount = base_price * (coupon.coupon_value / 100)
                elif coupon.coupon_type == "fixed_discount":
                    coupon_discount = coupon.coupon_value
            
            # Final cost calculation
            total_cost = base_price - normal_discount - coupon_discount
            
            booking = {}
            booking['car'] = car
            booking['user'] = user
            booking['car_title'] = f"{car.car_make.name} {car.car_model.name} {car.car_version}"
            booking['user_email'] = user.email
            booking['booking_type'] = booking_type
            booking['status'] = "pending"
            booking['start_date'] = start_date
            booking['end_date'] = end_date
            booking['pickup_date'] = pickup_date
            booking['pickup_time'] = pickup_time
            booking['with_driver'] = with_driver
            booking['additional_notes'] = additional_notes
            booking['coupon'] = coupon
            booking['coupon_code'] = coupon_code
            booking['driver_fee'] = driver_fee            
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
