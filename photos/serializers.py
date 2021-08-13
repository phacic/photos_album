from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Photo, Album

User = get_user_model()


class PhotoSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Photo
        fields = ('id', 'title', 'image', 'user', 'albums')

    def validate_albums(self, albums):
        """ validate user owes albums """
        request = self.context.get('request')

        for album in albums:
            if album.user_id != request.user.id:
                raise ValidationError("User must owe assigned albums.")
        return albums

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        validated_data['user'] = user
        return super(PhotoSerializer, self).create(validated_data)


class AlbumSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Album
        fields = ('id', 'title', 'user', 'photos')

    def validate_photos(self, photos):
        """ make sure photos assigned are owned by user """
        request = self.context.get('request')

        for photo in photos:
            if photo.user_id != request.user.id:
                raise ValidationError("User must owe assigned photos")
        return photos

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        validated_data['user'] = user
        return super(AlbumSerializer, self).create(validated_data)
