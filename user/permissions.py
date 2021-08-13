from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser  # for type hinting
from rest_framework import permissions
from config.utils import is_authenticated

User = get_user_model()


class IsAccountOwner(permissions.BasePermission):
    """
    custom permission to allow only owners of an account to perform an action
    """

    def has_object_permission(self, request, view, obj: AbstractUser):
        if is_authenticated(request):
            return request.user.id == obj.id

        return False


class IsAccountOwnerOrAdmin(permissions.BasePermission):
    """
    custom permission to allow owners of an account or staff (superuser) to perform an action
    """

    def has_object_permission(self, request, view, obj: AbstractUser):
        if is_authenticated(request):
            account_owner = IsAccountOwner()
            return account_owner.has_object_permission(request, view, obj) or request.user.is_staff

        return False
