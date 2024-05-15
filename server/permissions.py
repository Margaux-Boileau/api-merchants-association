from rest_framework import permissions

"""
Custom permission to allow access only to admin users or owners working at the shop.
"""

class IsAuthenticatedOrOwner(permissions.BasePermission):    
    
    def has_permission(self, request, view):
        print('CHECK: has_permission')
        # Check if the user is an admin or an owner of a shop
        return bool(request.user and (request.user.is_admin or request.user.is_owner_of_shop))