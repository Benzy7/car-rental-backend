import django_filters
from core.models.car import Car

class CarFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price_per_day', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price_per_day', lookup_expr='lte')

    class Meta:
        model = Car
        fields =  ['car_make', 'car_type', 'fuel_type', 'transmission_type', 'seats', 'min_price', 'max_price'] 

class CarModelFilter(django_filters.FilterSet):
    fuel_type = django_filters.CharFilter(
        field_name="cars_of_model__fuel_type", 
        method="filter_multiple_values"
    )
    transmission_type = django_filters.CharFilter(
        field_name="cars_of_model__transmission_type", 
        method="filter_multiple_values"
    )
    seats = django_filters.CharFilter(
        field_name="cars_of_model__seats", 
        method="filter_multiple_values"
    )
    car_type = django_filters.CharFilter(
        field_name="cars_of_model__car_type", 
        method="filter_multiple_values"
    )
    car_make = django_filters.CharFilter(
        field_name="cars_of_model__car_make__name", 
        method="filter_multiple_values"
    )
    min_price = django_filters.NumberFilter(
        field_name="cars_of_model__price_per_day", lookup_expr='gte'
    )
    max_price = django_filters.NumberFilter(
        field_name="cars_of_model__price_per_day", lookup_expr='lte'
    )

    class Meta:
        model = Car
        fields = ['fuel_type', 'transmission_type', 'seats', 'car_type', 'car_make', 'min_price', 'max_price']

    def filter_multiple_values(self, queryset, name, value):

        values = value.split(',')
        return queryset.filter(**{f"{name}__in": values})
