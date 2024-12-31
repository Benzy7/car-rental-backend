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

# TODO
class CarFeatureViewSet(viewsets.ModelViewSet):
    queryset = CarFeature.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CarFeatureListSerializer
        elif self.action == 'retrieve':
            return CarFeatureRetrieveSerializer
        return CarFeatureCreateUpdateSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsNotBlacklisted(), IsAdminUserRole()]
        return [IsAuthenticated(), IsNotBlacklisted()] 

class BookCarFeaturesAPIView(APIView):
    permission_classes = []

    def get(self, request):
        try:
            features = CarFeature.objects.filter(is_active=True).only('id', 'name', 'price')
            serializer = BookCarFeatureReadSerializer(features, many=True)
            return Response({"info": "CAR_FEATURES_FETCHED_SUCCESSFULLY", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            exception_log(e,__file__)
            return Response({"info": "UNEXPECTED_ERROR_OCCURRED", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
