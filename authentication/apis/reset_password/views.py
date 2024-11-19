from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from core.utils.logger import exception_log
from core.utils.code_generator import generate_reset_pass_code
from core.utils.mailer import send_email
from core.models.user import User
from core.models.pin_code import PinCode
from authentication.serializers.user.reset_password import ResetPasswordRequestSerializer, ResetPasswordSerializer

class ResetPasswordRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = ResetPasswordRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            email = serializer.validated_data['email']
            
            user = User.objects.get(email=email)
    
            pin_code = generate_reset_pass_code(user)
            cuurent_year = timezone.now().year
            email_data = {
                'year': cuurent_year,
                'code': pin_code
            }
            send_email(user.email, "Demande de réinitialisation du mot de passe", "reset_password.html", email_data)

            return Response({"info": "RESET_PASSWORD_EMAIL_SENT",}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"info": "USER_NOT_FOUND","details": "The user with the provided email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            exception_log(e, __file__)
            return Response({"info": 'VALIDATION_ERROR',"details": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exception_log(e, __file__)
            return Response({"info": "UNEXPECTED_ERROR_OCCURRED","details": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = ResetPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            email = serializer.validated_data['email']
            pin_code = serializer.validated_data['pin_code']
            new_password = serializer.validated_data['new_password']
            
            user = User.objects.filter(email=email).first()
            if not user:
                return Response({"info": "USER_NOT_FOUND", "details": "No user found with the provided email address."}, status=status.HTTP_404_NOT_FOUND)

            latest_pin_code = PinCode.objects.filter(user=user, code=pin_code, is_used=False).order_by('-created_at').first()
            if not latest_pin_code:
                return Response({"info": "INVALID_PIN_CODE", "details": "The provided PIN code is invalid or has already been used."}, status=status.HTTP_400_BAD_REQUEST)
            
            if latest_pin_code.is_expired(5):
                return Response({"info": "PIN_CODE_EXPIRED", "details": "The provided PIN code has expired."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            latest_pin_code.is_used = True
            latest_pin_code.save()

            return Response({"info": "PASSWORD_RESET_SUCCESS", "message": "Your password has been successfully changed."}, status=status.HTTP_200_OK)
        except ValidationError as e:
            exception_log(e, __file__)
            return Response({"info": 'VALIDATION_ERROR', "details": str(e.detail)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exception_log(e, __file__)
            return Response({"info": "UNEXPECTED_ERROR_OCCURRED", "details": "Something went wrong while processing your request."}, status=status.HTTP_400_BAD_REQUEST)
