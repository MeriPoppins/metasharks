from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Role


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            request.user.role == Role.ADMIN
        )


class IsTutor(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            request.user.role == Role.TUTOR
        )
