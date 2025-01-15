from rest_framework.permissions import BasePermission
from core.models import Partner

class IsAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            if request.user.role == 'admin':
                return True
            
            partner_id = request.data.get('partner')
            if partner_id:
                try:
                    partner = Partner.objects.filter(id=partner_id).only('id').first()
                    print(partner)
                    return partner.manager == request.user
                except Partner.DoesNotExist:
                    return False
    
            return False
        
        # For other methods (GET, PUT, PATCH, DELETE), allow the request to proceed
        # The object-level permission will be checked in `has_object_permission`
        return True

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' or (
            request.user.role == 'partner' and obj and obj.partner and obj.partner.manager == request.user
        )
