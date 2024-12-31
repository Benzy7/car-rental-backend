from django.urls import path, include
from rest_framework.routers import DefaultRouter
from automobile.apis import CarMakeViewSet, TopCarMakesAPIView, CarModelViewSet, CarModelImageViewSet, \
    CarViewSet, ImportCarsView, CarListByModelAPIView, CarImageViewSet, ExploreCarsAPIView

router = DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'car-makes', CarMakeViewSet)
router.register(r'car-models', CarModelViewSet)
router.register(r'car-images', CarImageViewSet)
router.register(r'car-model-images', CarModelImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('top-car-makes/', TopCarMakesAPIView.as_view(), name='top-car-makes'),
    path('explore/', ExploreCarsAPIView.as_view(), name='explore-cars'),
    path('cars-by-model/', CarListByModelAPIView.as_view(), name='car-list-by-model'),
    path('import-cars/', ImportCarsView.as_view(), name='import-cars'),
]
