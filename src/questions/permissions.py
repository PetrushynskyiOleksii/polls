"""Custom permissions for question app."""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Object-level permission to only allow owners of an object to edit it."""

    def has_object_permission(self, request, view, obj):
        """Return true if user is owner or request method in safe methods."""
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check permission for question view
        if hasattr(obj, 'user'):
            object_owner = obj.user
        # Check permission for answer view
        else:
            object_owner = obj.question.user

        return object_owner == request.user
