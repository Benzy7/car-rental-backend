from rest_framework import serializers

class NewBookingSerializer(serializers.Serializer):
    car_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    pickup_time = serializers.TimeField(required=True)    
    return_time = serializers.TimeField(required=True)    
    with_driver = serializers.BooleanField(required=False)
    coupon_code = serializers.CharField(required=False)
    booking_type = serializers.CharField(required=True)
    additional_notes = serializers.CharField(required=False)
    flight_number = serializers.CharField(required=False)
    plane_arrival_datetime = serializers.DateTimeField(required=False)
    airport_id = serializers.IntegerField(required=False)
    transfer_destination_id = serializers.IntegerField(required=False)
    