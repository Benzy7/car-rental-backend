from django.db import models
from core.models.user import User
from core.models.car import Car

class FavoriteCar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_cars")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="favorited_by")
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')
