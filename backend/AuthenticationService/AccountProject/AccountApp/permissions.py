
from rest_framework.permissions import BasePermission


class IsVerifyUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_verify:
            return True
        return False


class IsOwnerOrIsAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        return obj.id == request.user.id or request.user.is_staff
