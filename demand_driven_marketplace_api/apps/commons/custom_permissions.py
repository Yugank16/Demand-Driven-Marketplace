from rest_framework.permissions import BasePermission


class AllowAnonymous(BasePermission):

    def has_permission(self, request, view):
        """
        Permission for anonymous users only
        """
        return bool(request.user and not request.user.is_authenticated)
