from rest_framework.permissions import BasePermission
    
# ONLY FOR: retrieve, update, partial_update, and destroy
class IsAdminOrOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or (obj and obj.manager and obj.manager == request.user)
