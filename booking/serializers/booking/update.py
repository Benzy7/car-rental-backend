from rest_framework import serializers

class ActionBookingSerializer(serializers.Serializer):
    action = serializers.CharField(required=True)
    new_end_date = serializers.DateField(required=False)
    cancel_reason = serializers.CharField(required=False)
    extension_decision = serializers.CharField(required=False)
