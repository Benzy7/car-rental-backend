from rest_framework import serializers

class NewBookingSerializer(serializers.Serializer):
    car_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)
    features = serializers.ListField(child=serializers.IntegerField(), required=False)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    pickup_time = serializers.TimeField(required=True)    
    return_time = serializers.TimeField(required=True)    
    with_driver = serializers.BooleanField(required=False)
    coupon_code = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    booking_type = serializers.CharField(required=True)
    phone_number_1 = serializers.CharField(required=True)
    phone_number_2 = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    additional_notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    flight_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    plane_arrival_datetime = serializers.DateTimeField(required=False, allow_null=True)
    airport_id = serializers.IntegerField(required=False, allow_null=True)
    transfer_destination_id = serializers.IntegerField(required=False, allow_null=True)
    