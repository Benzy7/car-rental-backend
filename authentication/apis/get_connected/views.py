from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from authentication.serializers.user.user_profile import UserProfileSerializer
from core.utils.logger import exception_log
from core.models.referral_code import ReferralCode
from core.utils.code_generator import generate_user_referral_code

class GetConnectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            current_user = request.user
            current_user_serializer = UserProfileSerializer(current_user)
                            
            referral_code_value = None
            try:
                referral_code, created = ReferralCode.objects.get_or_create(
                    user=current_user,
                    defaults={'user_email': current_user.email}  
                )
                if created:
                    referral_code.referral_code = generate_user_referral_code(current_user)
                    referral_code.save(update_fields=['referral_code', 'used_by_email'])
                referral_code_value = referral_code.referral_code
            except Exception as ref_exception:
                exception_log(ref_exception,__file__)
                
            return Response({
                "info": "USER_FETCHED_SUCCESS", 
                "user": current_user_serializer.data,
                "referral_code": referral_code_value
            }, status=status.HTTP_200_OK)
        except Exception as e:
            exception_log(e,__file__)
            return Response({"info": "UNEXPECTED_ERROR_OCCURRED","details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
