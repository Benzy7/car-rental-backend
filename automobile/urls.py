from django.urls import path, include
from rest_framework.routers import DefaultRouter
from automobile.apis import CarMakeViewSet, TopCarMakesAPIView, CarModelViewSet, CarImageViewSet, CarViewSet

router = DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'car-makes', CarMakeViewSet)
router.register(r'car-models', CarModelViewSet)
router.register(r'car-model-images', CarImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('top-car-makes/', TopCarMakesAPIView.as_view(), name='top-car-makes'),
]
