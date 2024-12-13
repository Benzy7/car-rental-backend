from django.urls import path
from booking.apis import NewBookingView

urlpatterns = [
    path('new-booking/', NewBookingView.as_view(), name='create-booking'),
]
