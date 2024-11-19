import django_filters
from core.models.car import Car

class CarFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price_per_day', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price_per_day', lookup_expr='lte')

    class Meta:
        model = Car
        fields =  ['car_make', 'car_type', 'fuel_type', 'transmission_type', 'seats', 'min_price', 'max_price'] 