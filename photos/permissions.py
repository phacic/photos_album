from typing import Union
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser  # for type hinting
from rest_framework import permissions
from .models import Photo, Album
from config.utils import is_authenticated

User = get_user_model()


class IsPhotoOrAlbumOwner(permissions.BasePermission):
    """
    permission to allow only owner of a photo to perform an action
    """

    def has_object_permission(self, request, view, obj: Union[Album, Photo]):
        if is_authenticated(request):
            return request.user.id == obj.user_id

        return False


class IsPhotoOrAlbumOwnerOrAdmin(permissions.BasePermission):
    """
    permission to allow only owner of a photo to perform an action
    """

    def has_object_permission(self, request, view, obj: Union[Album, Photo]):
        if is_authenticated(request):
            photo_owner = IsPhotoOrAlbumOwner()
            return photo_owner.has_object_permission(request, view, obj) or request.user.is_staff

        return False
