from django.urls import path, include
from rest_framework.routers import DefaultRouter
from automobile.apis import CarMakeViewSet, TopCarMakesAPIView, CarModelViewSet, CarModelImageViewSet, CarViewSet, ImportCarsView

router = DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'car-makes', CarMakeViewSet)
router.register(r'car-models', CarModelViewSet)
router.register(r'car-model-images', CarModelImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('top-car-makes/', TopCarMakesAPIView.as_view(), name='top-car-makes'),
    path('import-cars/', ImportCarsView.as_view(), name='import-cars'),
]
