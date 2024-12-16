from django.urls import path, include
from rest_framework.routers import DefaultRouter
from booking.apis import NewBookingView, AirportViewSet, GenerateAirportTransferDataView, TransferDestinationViewSet

router = DefaultRouter()
router.register(r'airports', AirportViewSet)
router.register(r'transfer-destinations', TransferDestinationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('new-booking/', NewBookingView.as_view(), name='create-booking'),
    path('generate-transfer-data/', GenerateAirportTransferDataView.as_view(), name='generate-transfer-data'),
]
