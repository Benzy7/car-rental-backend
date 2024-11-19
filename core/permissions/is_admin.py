from rest_framework import permissions

class IsAdminUserRole(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user.role == 'admin'
