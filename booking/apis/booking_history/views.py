from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from core.models.car_booking import CarBooking
from booking.serializers.booking.read import UserBookingHistorySerializer
from core.permissions.is_not_blacklisted import IsNotBlacklisted
from core.utils.logger import exception_log

class UserBookingsHistoryView(APIView):
    permission_classes = [IsAuthenticated, IsNotBlacklisted]
    
    def get(self, request, status_filter, *args, **kwargs):
        try:
            user = request.user

            if status_filter not in ('upcoming', 'completed', 'cancelled',):
                return Response({"info": "INVALID_BOOKING_STATUS"}, status=status.HTTP_400_BAD_REQUEST)

            bookings = []
            if status_filter == 'upcoming':
                bookings = CarBooking.objects.filter(user=user, status__in=['pending', 'confirmed']).select_related('car', 'airport', 'transfer_destination')
            elif status_filter == 'completed':
                bookings = CarBooking.objects.filter(user=user, status='completed').select_related('car', 'airport', 'transfer_destination')
            elif status_filter == 'cancelled':
                bookings = CarBooking.objects.filter(user=user, status='cancelled').select_related('car', 'airport', 'transfer_destination')
                
            serializer = UserBookingHistorySerializer(bookings, many=True)
            return Response({"info": "BOOKINGS_FETCHED_SUCCESSFULLY", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            exception_log(e,__file__)
            return Response({"info": "UNEXPECTED_ERROR_OCCURRED", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
