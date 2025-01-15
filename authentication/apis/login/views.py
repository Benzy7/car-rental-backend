from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.utils import timezone
from authentication.serializers.user.user_login import UserLoginSerializer
from authentication.serializers.user.user_refresh import UserRefreshTokenSerializer
from core.utils.logger import exception_log
from core.models.user import User
from core.models.referral_code import ReferralCode
from authentication.serializers.user.user_profile import UserProfileSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user_check = User.objects.filter(email=email).only('is_active', 'is_complete', 'is_blacklisted').first()
            if not user_check:
                return Response({"info": "NO_ACCOUNT_FOUND"}, status=status.HTTP_404_NOT_FOUND)

            if user_check.is_blacklisted:
                return Response({
                    "info": "BLACKLISTED_ACCOUNT", 
                    "details": "Your account has been blacklisted. Please contact support for more information."
                }, status=status.HTTP_403_FORBIDDEN)
                
            if not user_check.is_complete:
                return Response({"info": "INCOMPLETE_ACCOUNT"}, status=status.HTTP_400_BAD_REQUEST)
            
            if not user_check.is_active:
                return Response({"info": "DEACTIVATED_ACCOUNT"}, status=status.HTTP_400_BAD_REQUEST)
    
            user = authenticate(username=email, password=password)
            if not user:
                return Response({"info": "INVALID_CREDENTIALS"}, status=status.HTTP_400_BAD_REQUEST)
            
            refresh = RefreshToken.for_user(user)
            
            user.last_login = timezone.now()
            user.save(update_fields=['last_login']) 
            
            user_serializer = UserProfileSerializer(user)
            referral_code_value = None
            referral_code = ReferralCode.objects.filter(user=user).first()
            if referral_code:
                referral_code_value = referral_code.referral_code

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_serializer.data,
                'referral_code': referral_code_value,
                'info': 'LOGIN_SUCCESS'
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            exception_log(e, __file__)
            return Response({"info": 'CREDENTIALS_VALIDATION_ERROR', "details": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exception_log(e,__file__)
            return Response({"info": "UNEXPECTED_ERROR_OCCURRED", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#TODO: retest refresh
class TokenRefreshView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRefreshTokenSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            refresh_token = serializer.validated_data['refresh']
            
            refresh = RefreshToken(refresh_token)
            
            user_id = refresh.payload.get('user_id')  
            user = User.objects.get(pk=user_id)  
            if user.is_blacklisted:
                return Response({
                    "info": "BLACKLISTED_ACCOUNT", 
                    "details": "Your account has been blacklisted and you cannot access this service. Please contact support for further details."
                }, status=status.HTTP_403_FORBIDDEN)
            
            new_refresh_token = RefreshToken.for_user(user)
            refresh.blacklist()  
            new_access_token = new_refresh_token.access_token
            
            return Response({'access': str(new_access_token), 'refresh': str(new_refresh_token)}, status=status.HTTP_200_OK)
        except ValidationError as e:
            exception_log(e, __file__)
            return Response({"info": 'REFRESH_TOKEN_VALIDATION_ERROR', "details": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError as e:
            exception_log(e, __file__)
            return Response({"info": "INVALID_REFRESH_TOKEN", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exception_log(e, __file__)
            return Response({"info": "ERROR_REFRESHING_TOKEN", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
