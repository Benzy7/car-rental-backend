from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from django.db import transaction
from authentication.serializers.user.user_register import ClientRegisterSerializer
from core.utils.logger import exception_log
from core.utils.code_generator import generate_referral_code
from core.models.referral_code import ReferralCode

class RegisterClientView(generics.CreateAPIView):
    serializer_class = ClientRegisterSerializer
    permission_classes = [AllowAny]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save() 
            
            try:
                user_referral_code = generate_referral_code(user, code_type='user')
                ReferralCode.objects.create(user=user, referral_code=user_referral_code, user_email=user.email)
            except Exception as e:
                exception_log(e,__file__)

            return Response({"info": "USER_CREATED_SUCCESSFULLY", "user": serializer.data}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            exception_log(e,__file__)
            transaction.set_rollback(True)
            return Response({"info": 'VALIDATION_ERROR', "details": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exception_log(e,__file__)
            transaction.set_rollback(True)
            return Response({"info": "UNEXPECTED_ERROR_OCCURRED", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
