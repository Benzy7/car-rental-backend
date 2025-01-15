from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from core.models import CarBooking
from core.utils.logger import exception_log
from core.utils.booking import check_booking_action_permissions
from core.permissions.is_not_blacklisted import IsNotBlacklisted
from booking.serializers.booking.update import ActionBookingSerializer

class BookingActionAPIView(APIView):
    serializer_class = ActionBookingSerializer
    permission_classes = [IsAuthenticated, IsNotBlacklisted]

    @transaction.atomic
    def post(self, request, booking_id):
        try:
            action = request.data.get('action')
            new_end_date = request.data.get('new_end_date', None)
            cancel_reason = request.data.get('cancel_reason', "")
            extension_decision = request.data.get('extension_decision', "")

            booking = CarBooking.objects.filter(id=booking_id).only(
                'booking_type', 'status', 'start_date', 'confirmed_date', 'cancelled_date', 'cancel_reason', 'end_date', 
                'car', 'extension_status', 'extension_end_date', 'final_total_cost', 'extension_cost'
            ).first()
            if not booking:
                return Response({"info": "BOOKING_NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)
            
            # Check user permissions based on action
            is_allowed = check_booking_action_permissions(request.user, action, booking)
            if not is_allowed:
                return Response({"detail": "You do not have permission to do this action."}, status=status.HTTP_403_FORBIDDEN)

            if action == 'confirm':
                return self.confirm_booking(booking)
            elif action == 'cancel':
                # if not cancel_reason:
                #     raise ValidationError("Cancel reason is required for canceling a booking.")
                return self.cancel_booking(booking, cancel_reason)
            elif action == 'extension_request':
                if not new_end_date:
                    raise ValidationError("New end date is required for extending a booking.")
                return self.extend_booking_request(booking, new_end_date)
            elif action == 'extension_review':
                if extension_decision not in ['accept', 'reject']:
                    raise ValidationError("Invalid extension decision.")
                return self.extend_booking_review(booking, extension_decision)
            else:
                raise ValidationError("Invalid action specified.")
        except ValidationError as e:
            exception_log(e,__file__)
            transaction.set_rollback(True)
            return Response({"info": 'VALIDATION_ERROR', "details": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exception_log(e,__file__)
            transaction.set_rollback(True)
            return Response({"info": "UNEXPECTED_ERROR_OCCURRED", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def confirm_booking(self, booking):
        if booking.status == 'confirmed':
            return Response({"info": 'BOOKING_ALREADY_CONFIRMED'}, status=status.HTTP_400_BAD_REQUEST)
        
        booking.confirmed_date = timezone.now()
        booking.status = 'confirmed'
        booking.save(update_fields=['status', 'confirmed_date'])
        
        return Response({"info": 'BOOKING_CONFIRMED_SUCCESSFULLY'}, status=status.HTTP_200_OK)

    def cancel_booking(self, booking, cancel_reason):
        # #TODO add to params/ CANCEL FEE
        current_time = timezone.now()
        # cancel_window = timedelta(hours=24)  # 24-hour cancellation window
        # if booking.start_date - current_time <= cancel_window:
        #     return Response({"detail": "Cancellation not allowed within 24 hours of the booking."}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = 'cancelled'
        booking.cancelled_date = current_time
        booking.cancel_reason = cancel_reason
        booking.save(update_fields=['status', 'cancelled_date', 'cancel_reason'])
        
        return Response({"info": 'BOOKING_CANCELED_SUCCESSFULLY'}, status=status.HTTP_200_OK)
        
    def extend_booking_request(self, booking, new_end_date):
        if booking.booking_type not in ('standard', 'utility'):
            return Response({
                "info": "BOOKING_TYPE_NOT_EXTENDABLE", 
                "details": f"Booking type '{booking.booking_type}' is not eligible for extensions."
            }, status=status.HTTP_400_BAD_REQUEST)

        if new_end_date <= booking.end_date:
            return Response({"info": "EXTENSION_DATE_ERROR", "details": "New end date must be after the original end date."}, status=status.HTTP_400_BAD_REQUEST)

        overlapping_booked_cars_count = CarBooking.objects.filter(
            car=booking.car,
            status__in=['in_progress', 'confirmed', 'pending'],
            start_date__lte=new_end_date,
            end_date__gte=booking.start_date
        ).exclude(id=booking.id).count()
        available_cars = booking.car.max_available - overlapping_booked_cars_count

        if available_cars < 1:  
            return Response({"info": "CAR_UNAVAILABLE_ERROR", "details": "Car unavailable for the selected dates."}, status=status.HTTP_400_BAD_REQUEST)

        booking.extension_status = 'pending' 
        booking.extension_end_date = new_end_date
        booking.save(update_fields=['new_end_date'])
    
        return Response({"info": 'BOOKING_EXTENSION_REQUESTED'}, status=status.HTTP_200_OK)

    def extend_booking_review(self, booking, extension_decision):
        if extension_decision == 'accept':
            overlapping_booked_cars_count = CarBooking.objects.filter(
                car=booking.car,
                status__in=['in_progress', 'confirmed', 'pending'],
                start_date__lte=booking.extension_end_date,
                end_date__gte=booking.start_date
            ).exclude(id=booking.id).count()
            available_cars = booking.car.max_available - overlapping_booked_cars_count

            if available_cars < 1:  
                return Response({"info": "CAR_ALREADY_BOOKED"}, status=status.HTTP_400_BAD_REQUEST)

            nb_extended_days = (booking.extension_end_date - booking.end_date).days
            extension_cost = float(booking.extension_cost) + (float(booking.car.price_per_day)  * nb_extended_days)
            
            booking.extension_cost = extension_cost         
            booking.final_total_cost = float(booking.final_total_cost) + extension_cost
            booking.extension_status = 'accepted'         
            booking.end_date = booking.extension_end_date
            booking.save(update_fields=['extension_status', 'end_date', 'extension_cost', 'final_total_cost'])
        else:
            booking.extension_status = 'rejected'         
            booking.save(update_fields=['extension_status'])

        return Response({"info": 'BOOKING_EXTENSION_UPDATED'}, status=status.HTTP_200_OK)
