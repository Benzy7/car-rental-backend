from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction
from authentication.serializers.client.client_update import ClientUpdateSerializer
from authentication.serializers.client.client_complete import ClientCompletionSerializer
from core.utils.logger import exception_log
from core.models.user import User
from core.permissions.is_not_blacklisted import IsNotBlacklisted


class CompleteClientView(generics.UpdateAPIView):
    serializer_class = ClientCompletionSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        email = self.request.data.get('email') 
        return User.objects.get(email=email)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            if user.is_complete:    
                return Response({"info": "UNAUTHORIZED", "details": "This action cannot be performed."}, status=status.HTTP_401_UNAUTHORIZED)
            
            user.is_complete = True    
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

class UpdateClientView(generics.UpdateAPIView):
    serializer_class = ClientUpdateSerializer
    permission_classes = [IsAuthenticated, IsNotBlacklisted]

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
