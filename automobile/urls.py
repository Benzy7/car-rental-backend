from django.urls import path, include
from rest_framework.routers import DefaultRouter
from automobile.apis import CarMakeViewSet, TopCarMakesAPIView, CarModelViewSet, CarModelImageViewSet, FavoriteCarView, \
    CarViewSet, ImportCarsView, CarListByModelAPIView, CarImageViewSet, ExploreCarsAPIView, CarFeatureViewSet, BookCarFeaturesAPIView

router = DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'car-makes', CarMakeViewSet)
router.register(r'car-models', CarModelViewSet)
router.register(r'car-images', CarImageViewSet)
router.register(r'car-model-images', CarModelImageViewSet)
router.register(r'car-features', CarFeatureViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('top-car-makes/', TopCarMakesAPIView.as_view(), name='top-car-makes'),
    path('booking-car-features/', BookCarFeaturesAPIView.as_view(), name='car-features'),
    path('explore/', ExploreCarsAPIView.as_view(), name='explore-cars'),
    path('cars-by-model/', CarListByModelAPIView.as_view(), name='car-list-by-model'),
    path('favorite-cars/', FavoriteCarView.as_view(), name='favorite-cars'),
    path('import-cars/', ImportCarsView.as_view(), name='import-cars'),
]
