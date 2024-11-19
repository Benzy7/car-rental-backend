from django.contrib import admin
from core.models.car import Car, CarImage, CarMake, CarModel
from core.models.user import User
from core.models.pin_code import PinCode
from core.models.referral_code import ReferralCode, ReferralCodeUsage

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Car._meta.get_fields() if not field.many_to_many and not field.one_to_many]    
    list_per_page = 10 
    search_fields = ['car_make', 'car_model']
    ordering = ['created_at']
    list_display_links = ('created_at', 'updated_at')
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

@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CarImage._meta.get_fields() if not field.many_to_many and not field.one_to_many]    
    search_fields = ['car__car_make__name', 'car__car_model__name']
    ordering = ['created_at']
    list_display_links = ('created_at', 'updated_at')
    list_per_page = 10 

@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CarMake._meta.get_fields() if not field.many_to_many and not field.one_to_many]    
    search_fields = ['name']
    ordering = ['created_at']
    list_display_links = ('created_at', 'updated_at')
    list_filter = ('is_top',)
    list_per_page = 20 

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CarModel._meta.get_fields() if not field.many_to_many and not field.one_to_many]    
    search_fields = ['name']
    ordering = ['created_at']
    list_display_links = ('created_at', 'updated_at')
    list_filter = ('make',)
    list_per_page = 20 

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.get_fields() if not field.many_to_many and not field.one_to_many]    
    search_fields = ['email', 'phone_number', 'first_name', 'last_name' ]
    ordering = ['created_at']
    list_display_links = ('email', 'first_name', 'last_name', 'created_at', 'updated_at', 'phone_number')
    list_filter = ('role', 'gender', 'is_profile_complete', 'is_active',)
    list_per_page = 20 
    
@admin.register(PinCode)
class PinCodeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PinCode._meta.get_fields() if not field.many_to_many and not field.one_to_many]    
    search_fields = ['code' ]
    ordering = ['created_at']
    list_display_links = ('created_at', 'updated_at',)
    list_filter = ('is_used', 'code_type',)
    list_per_page = 20 

@admin.register(ReferralCode)
class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ReferralCode._meta.get_fields() if not field.many_to_many and not field.one_to_many]    
    search_fields = ['code' ]
    ordering = ['created_at']
    list_display_links = ('created_at', 'updated_at', 'usage_count', 'user_email')
    list_filter = ('is_active',)
    list_per_page = 20 

@admin.register(ReferralCodeUsage)
class ReferralCodeUsageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ReferralCodeUsage._meta.get_fields() if not field.many_to_many and not field.one_to_many]    
    search_fields = ['code' ]
    ordering = ['created_at']
    list_display_links = ('created_at', 'updated_at', 'used_by_email',)
    list_filter = ('is_claimed', 'referral_code',)
    list_per_page = 20 