from django.contrib import admin
from core.models.user import User
from core.models.pin_code import PinCode
from core.models.referral_code import ReferralCode, ReferralCodeUsage

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.get_fields() if not field.many_to_many and not field.one_to_many and field.name != 'password']    
    search_fields = ['email', 'phone_number', 'first_name', 'last_name' ]
    ordering = ['created_at']
    list_display_links = ('id',)
    list_filter = ('role', 'gender', 'is_verified', 'is_active',)
    list_per_page = 20 
    
# @admin.register(PinCode)
# class PinCodeAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in PinCode._meta.get_fields() if not field.many_to_many and not field.one_to_many]    
#     search_fields = ['code' ]
#     ordering = ['created_at']
#     list_display_links = ('id',)
#     list_filter = ('is_used', 'code_type',)
#     list_per_page = 20 

@admin.register(ReferralCode)
class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ReferralCode._meta.get_fields() if not field.many_to_many and not field.one_to_many]    
    search_fields = ['code' ]
    ordering = ['created_at']
    list_display_links = ('id',)
    list_filter = ('is_active',)
    list_per_page = 20 

# @admin.register(ReferralCodeUsage)
# class ReferralCodeUsageAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in ReferralCodeUsage._meta.get_fields() if not field.many_to_many and not field.one_to_many]    
#     search_fields = ['code' ]
#     ordering = ['created_at']
#     list_display_links = ('id',)
#     list_filter = ('referral_code',)
#     list_per_page = 20 