from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Photo, Album

User = get_user_model()


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'title', 'image', 'user', 'albums')

    def validate_albums(self, albums):
        """ validate user owes albums """

        for album in albums:
            if album.user_id != self.context.request.user.id:
                raise ValidationError("User must owe assigned album.")
        return albums


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'
