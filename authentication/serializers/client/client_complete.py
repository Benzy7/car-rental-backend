from rest_framework import serializers
from core.models.user import User, Gender
from core.models.parameters import Parameters
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

class ClientCompletionSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    gender = serializers.ChoiceField(choices=Gender)

    class Meta:
        model = User
        fields = [
            'email', 'country', 'phone_country_code', 'phone_number', 'birthday',
            'gender', 'profile_picture', 'driver_licence_picture', 'passport_picture',
        ]
        extra_kwargs = {
            'email': {'required': True},
            'phone_country_code': {'required': True},
            'phone_number': {'required': True},
            'country':  {'required': True},
        }

    def validate_profile_picture(self, value):
        if value is not None:
            params = Parameters.get_instance(fields=['profile_picture_size'])
            max_size = params.profile_picture_size * 1024 * 1024
            if value.size > max_size:
                raise serializers.ValidationError(f"The image size should not exceed {params.profile_picture_size} MB.")
        return value
    
    def update(self, instance, validated_data):
        profile_picture = validated_data.pop('profile_picture', None)
        if profile_picture:
            img = Image.open(profile_picture)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            img.thumbnail((300, 300))
            
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=85) 
            buffer.seek(0)
            
            filename = f"{instance.first_name}_{instance.last_name}.jpg"
            instance.profile_picture.save(filename, ContentFile(buffer.read()), save=False)

        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance
