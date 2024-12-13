from django.urls import path, include
from rest_framework.routers import DefaultRouter
from partners.apis import PartnerViewSet

router = DefaultRouter()
router.register(r'partner', PartnerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
