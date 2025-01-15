from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from core.utils.logger import exception_log
from core.models.car_feature import CarFeature
from core.permissions.is_admin import IsAdminUserRole
from core.permissions.is_not_blacklisted import IsNotBlacklisted
from automobile.serializers.car_feature.create_or_update import CarFeatureCreateUpdateSerializer
from automobile.serializers.car_feature.read import CarFeatureRetrieveSerializer, CarFeatureListSerializer, BookCarFeatureReadSerializer

class CarFeatureViewSet(viewsets.ModelViewSet):
    queryset = CarFeature.objects.all()
    permission_classes = [IsAuthenticated, IsNotBlacklisted, IsAdminUserRole]

    def get_serializer_class(self):
        if self.action == 'list':
            return CarFeatureListSerializer
        elif self.action == 'retrieve':
            return CarFeatureRetrieveSerializer
        return CarFeatureCreateUpdateSerializer
    
    def finalize_response(self, request, response, *args, **kwargs):
        if not isinstance(response.data, (dict, list)):
            response.data = {
                "info": "UNEXPECTED_ERROR_OCCURRED",
                "errors": str(response.data)
            }
            return super().finalize_response(request, response, *args, **kwargs)
        
        if isinstance(response.data, (dict, list)) and 'info' in response.data:
            return super().finalize_response(request, response, *args, **kwargs)
        
        if response.status_code < 300:
            info = {
                'create': "CAR_FEATURE_CREATED_SUCCESSFULLY",
                'update': "CAR_FEATURE_UPDATED_SUCCESSFULLY",
                'partial_update': "CAR_FEATURE_UPDATED_SUCCESSFULLY",
                'retrieve': "CAR_FEATURE_RETRIEVED_SUCCESSFULLY",
                'list': "CAR_FEATURES_LISTED_SUCCESSFULLY",
                'destroy': "CAR_FEATURE_DELETED_SUCCESSFULLY"
            }.get(self.action, "SUCCESS")
                    
            response.data = {
                "info": info,
                "data": response.data
            }
        else: 
            info = "UNEXPECTED_ERROR_OCCURRED"
            if isinstance(response.data, dict) and 'detail' in response.data:
                if isinstance(response.data['detail'], list) or isinstance(response.data['detail'], dict):
                    info = "VALIDATION_ERROR"
            elif response.status_code == 404:
                info = "CAR_FEATURE_NOT_FOUND"      
                 
            response.data = {
                "info": info,
                "errors": response.data 
            } 
        return super().finalize_response(request, response, *args, **kwargs)

class BookCarFeaturesAPIView(APIView):
    permission_classes = []

    def get(self, request):
        try:
            features = CarFeature.objects.filter(is_active=True).only('id', 'code', 'price')
            serializer = BookCarFeatureReadSerializer(features, many=True)
            return Response({"info": "CAR_FEATURES_FETCHED_SUCCESSFULLY", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            exception_log(e,__file__)
            return Response({"info": "UNEXPECTED_ERROR_OCCURRED", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
