import django_filters
from core.models.car import Car, CarModel

class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass

class CarFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price_per_day', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price_per_day', lookup_expr='lte')
    car_class = CharInFilter(field_name='car_class', lookup_expr='in')
    car_make = CharInFilter(field_name='car_make', lookup_expr='in')
    car_model = CharInFilter(field_name='car_model', lookup_expr='in')
    car_type = CharInFilter(field_name='car_type', lookup_expr='in')
    fuel_type = CharInFilter(field_name='fuel_type', lookup_expr='in')
    transmission_type = CharInFilter(field_name='transmission_type', lookup_expr='in')

    class Meta:
        model = Car
        fields =  [
            'car_class', 'is_popular', 'is_top_pick', 'car_make', 'car_type', 'fuel_type', 'transmission_type',
            'seats', 'min_price', 'max_price', 'partner', 'is_active', 'country'
        ] 

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
        model = CarModel
        fields = ['fuel_type', 'transmission_type', 'seats', 'car_type', 'car_make', 'min_price', 'max_price']

    def filter_multiple_values(self, queryset, name, value):

        values = value.split(',')
        return queryset.filter(**{f"{name}__in": values})
