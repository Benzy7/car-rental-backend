from django.contrib import admin
from core.models.car import Car, CarModelImage, CarMake, CarModel

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Car._meta.get_fields() if not field.many_to_many and not field.one_to_many]    
    list_per_page = 10 
    search_fields = ['car_make', 'car_model']
    ordering = ['created_at']
    list_display_links = ('id',)

    list_filter = (
        'car_make',
        'car_model',
        'car_type',
        'car_class',
        'transmission_type',
        'fuel_type',
        'seats',
        'is_best',
        'is_top_pick',
        'is_top_rated',
        'is_recently_viewed',
        'has_exclusive_offer',
    )  
    # actions = ['make_discount']  # Add custom actions if needed

    # def make_discount(self, request, queryset):
    #     # Example action to apply discount on selected cars
    #     queryset.update(price=F('price') * 0.9)
    # make_discount.short_description = "Apply 10% discount to selected cars"

# @admin.register(CarModelImage)
# class CarModelImageAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in CarModelImage._meta.get_fields() if not field.many_to_many and not field.one_to_many]    
#     search_fields = ['car__car_make__name', 'car__car_model__name']
#     ordering = ['created_at']
#     list_display_links = ('id',)

#     list_per_page = 10 

@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CarMake._meta.get_fields() if not field.many_to_many and not field.one_to_many]    
    search_fields = ['name']
    ordering = ['created_at']
    list_display_links = ('id',)
    list_filter = ('is_top',)
    list_per_page = 20 

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CarModel._meta.get_fields() if not field.many_to_many and not field.one_to_many]    
    search_fields = ['name']
    ordering = ['created_at']
    list_display_links = ('id',)

    list_filter = ('make',)
    list_per_page = 20 
