from rest_framework import serializers

class NewBookingSerializer(serializers.Serializer):
    car_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)
    end_date = serializers.DateField(required=True)
    start_date = serializers.DateField(required=True)
    pickup_date = serializers.DateField(required=True)
    pickup_time = serializers.TimeField(required=True)    
    with_driver = serializers.BooleanField(required=False)
    coupon_code = serializers.CharField(required=False)
    booking_type = serializers.CharField(required=True)
    additional_notes = serializers.CharField(required=False)
