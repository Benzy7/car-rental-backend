from django.contrib import admin
from core.models.car_booking import CarBooking

@admin.register(CarBooking)
class CarBookingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CarBooking._meta.get_fields() if not field.many_to_many and not field.one_to_many]    
    list_per_page = 10 
    search_fields = ['car_make', 'car_model']
    ordering = ['created_at', 'updated_at', 'start_date', 'end_date']
    list_display_links = ('id',)
    list_filter = (
        'car',
        'user',
        'user_email',
        'booking_type',
        'status',
    )  
