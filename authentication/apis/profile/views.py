from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db import transaction
from authentication.serializers.user.user_register import ClientRegisterSerializer
from authentication.serializers.user.user_update import ClientUpdateSerializer
from core.utils.logger import exception_log
from core.utils.code_generator import generate_user_referral_code
from core.models.user import User
from core.models.referral_code import ReferralCode

class RegisterView(generics.CreateAPIView):
    serializer_class = ClientRegisterSerializer
    permission_classes = [permissions.AllowAny]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save() 
            
            try:
                user_referral_code = generate_user_referral_code(user)
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

class CompleteProfileView(generics.UpdateAPIView):
    serializer_class = ClientUpdateSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        email = self.request.data.get('email') 
        return User.objects.get(email=email)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            if user.is_profile_complete:    
                return Response({"info": "UNAUTHORIZED", "details": "This action cannot be performed."}, status=status.HTTP_401_UNAUTHORIZED)
            
            user.is_profile_complete = True    
            user.is_active = True

            serializer = self.get_serializer(data=request.data, instance=user)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({"info": "PROFILE_COMPLETED_SUCCESSFULLY", "user": serializer.data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"info": "USER_NOT_FOUND", "details": "The user with the provided email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            exception_log(e, __file__)
            transaction.set_rollback(True)
            return Response({"info": 'VALIDATION_ERROR', "details": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exception_log(e, __file__)
            transaction.set_rollback(True)
            return Response({"info": "UNEXPECTED_ERROR_OCCURRED", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = ClientUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data, instance=self.get_object())
            serializer.is_valid(raise_exception=True)

            req_email = serializer.validated_data.get('email')
            if req_email and req_email != user.email:
                return Response({"info": "UNAUTHORIZED", "details": "This action cannot be performed."}, status=status.HTTP_401_UNAUTHORIZED)

            serializer.save()
                   
            return Response({"info": "PROFILE_UPDATED_SUCCESSFULLY", "user": serializer.data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"info": "USER_NOT_FOUND", "details": "The user with the provided email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            exception_log(e, __file__)
            transaction.set_rollback(True)
            return Response({"info": 'VALIDATION_ERROR', "details": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exception_log(e, __file__)
            transaction.set_rollback(True)
            return Response({"info": "UNEXPECTED_ERROR_OCCURRED", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
