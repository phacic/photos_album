from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from rest_framework import viewsets, generics
from rest_framework import permissions
from . import permissions as user_permissions

from .serializers import (UserSerializer, SignUpSerializer)

User: AbstractUser = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    users view to list, get and update users
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    http_method_names = ('put', 'patch', 'get')

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        # only owners of account should be allow to update
        self.permission_classes = (user_permissions.IsAccountOwner,)
        return super(UserViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # owner or admin can delete account
        self.permission_classes = (user_permissions.IsAccountOwner,)
        return super().destroy(request, *args, **kwargs)


class SignUpView(generics.CreateAPIView):
    """
    sign up view
    """
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
