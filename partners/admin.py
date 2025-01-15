from django.contrib import admin
from core.models.partner import Partner

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Partner._meta.get_fields() if not field.many_to_many and not field.one_to_many]    
    list_per_page = 10 
    search_fields = ['email', 'name', 'phone_number']
    ordering = ['created_at', 'updated_at']
    list_display_links = ('id',)
    list_filter = (
        'is_active',
        'partner_type',
        'country'
    )  
