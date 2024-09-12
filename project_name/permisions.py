from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperUserForWrite(BasePermission):
    """
    Custom permission to only allow superusers to perform POST and PUT requests.
    """
    
    def has_permission(self, request, view):
        # Allow all users to perform SAFE_METHODS (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        
        # Allow only superusers for POST and PUT methods
        if request.method in ['POST', 'PUT', ' DELETE']:
            return request.user and request.user.is_superuser
        
        # Allow all other methods (e.g., DELETE) based on other logic if necessary
        return True