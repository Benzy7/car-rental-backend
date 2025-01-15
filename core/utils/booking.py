from rest_framework.exceptions import PermissionDenied
from datetime import timedelta
from django.utils import timezone
from core.models import CarBooking

def is_car_available(car, start_date, end_date, quantity=1):
    booked_cars_count = CarBooking.objects.filter(
        car=car,
        status__in=['in_progress', 'confirmed', 'pending'],
        start_date__lte=end_date,
        end_date__gte=start_date
    ).count()

    available_cars = car.max_available - booked_cars_count

    if available_cars >= quantity:
        return True

    return False


def check_booking_action_permissions(user, action, booking):
    if action == 'confirm':
        if not (user.role == 'admin' or booking.car.partner.manager == user):
            return False
    elif action == 'cancel':
        if not (user.role == 'admin' or booking.car.partner.manager == user or booking.user == user):
            return False
    elif action == 'extend':
        if not (user.role == 'admin' or booking.user == user):
            return False
    
    return True
