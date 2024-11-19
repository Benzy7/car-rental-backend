from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from authentication.serializers.user.user_login import UserLoginSerializer
from core.utils.logger import exception_log
from core.models.user import User

class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user_check = User.objects.filter(email=email).only('is_active', 'is_profile_complete').first()
            if user_check and not user_check.is_active:
                if not user_check.is_profile_complete:
                    return Response({"info": "INCOMPLETE_ACCOUNT"}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"info": "USER_INACTIVE"}, status=status.HTTP_400_BAD_REQUEST)
    
            user = authenticate(username=email, password=password)
            if not user:
                return Response({"info": "INVALID_CREDENTIALS"}, status=status.HTTP_400_BAD_REQUEST)
            
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'info': 'LOGIN_SUCCESS'
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            exception_log(e, __file__)
            return Response({"info": 'CREDENTIALS_VALIDATION_ERROR', "details": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exception_log(e,__file__)
            return Response({"info": "UNEXPECTED_ERROR_OCCURRED", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
