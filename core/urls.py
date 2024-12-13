from django.urls import path, include

urlpatterns = [
    path("auth/", include("authentication.urls")),
    path("auto/", include("automobile.urls")),
    path("corp/", include("partners.urls")),
    path("booking/", include("booking.urls")),
]
