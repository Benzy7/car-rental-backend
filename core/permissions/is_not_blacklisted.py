from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsNotBlacklisted(BasePermission):
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if getattr(request.user, 'is_blacklisted', False):
            raise PermissionDenied("Your account is blacklisted and cannot perform this action.")
        
        return True
