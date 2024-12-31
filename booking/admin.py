from django.contrib import admin
from django.db import transaction
from core.models.car_booking import CarBooking
from core.models.airport_transfer import Airport, TransferDestination

@admin.register(CarBooking)
class CarBookingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CarBooking._meta.get_fields() if not field.many_to_many and not field.one_to_many]    
    list_per_page = 10 
    search_fields = ['car_description', 'user_email', 'cancel_reason']
    ordering = ['created_at', 'updated_at', 'start_date', 'end_date']
    list_display_links = ('id',)
    list_filter = (
        'car',
        'user',
        'user_email',
        'booking_type',
        'status',
    )  

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Airport._meta.get_fields() if not field.many_to_many and not field.one_to_many]    
    search_fields = ['name']
    ordering = ['created_at', 'updated_at', 'name']
    list_display_links = ('id',)

@admin.register(TransferDestination)
class TransferDestinationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TransferDestination._meta.get_fields() if not field.many_to_many and not field.one_to_many]    
    search_fields = ['city']
    ordering = ['created_at', 'updated_at', 'price']
    list_display_links = ('id',)
    list_per_page = 10 
    list_filter = ('airport',) 
