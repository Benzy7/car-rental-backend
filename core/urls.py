from django.urls import path, include

urlpatterns = [
    path("auth/", include("authentication.urls")),
    path("auto/", include("automobile.urls")),
]
