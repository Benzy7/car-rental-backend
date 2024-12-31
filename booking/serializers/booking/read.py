from rest_framework import serializers
from core.models.car_booking import CarBooking
    
class UserBookingHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CarBooking
        fields = '__all__' 
        read_only_fields = tuple(field.name for field in model._meta.fields  if field.name != 'user')
        depth = 1  
