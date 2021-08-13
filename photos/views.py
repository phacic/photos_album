from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from config.utils import DynamicPagination
from .models import Photo, Album
from .serializers import PhotoSerializer, AlbumSerializer
from .permissions import IsPhotoOrAlbumOwner


class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer
    permission_classes = (permissions.IsAuthenticated, IsPhotoOrAlbumOwner)
    pagination_class = DynamicPagination

    def get_queryset(self):
        """ retrieve only photos created by user """
        return Photo.user_objects.queryset(self.request.user.id)


class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    permission_classes = (permissions.IsAuthenticated, IsPhotoOrAlbumOwner)
    pagination_class = DynamicPagination

    def get_queryset(self):
        """ retrieve only albums created by user """
        return Album.user_objects.queryset(self.request.user.id)

    @action(detail=True, methods=['patch'])
    def add_photos(self, request, *args, **kwargs):
        """ add multiple photos to album """

        album: Album = self.get_object()
        user = self.request.user
        photo_ids = list(set(self.request.data.get('photos')))

        # get photos from the ids that belong to user
        user_photos = Photo.user_objects.queryset(user_id=user.id).filter(id__in=photo_ids)

        for p in user_photos:
            album.photos.add(p)

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def remove_photos(self, request, *args, **kwargs):
        """ remove multiple photos to album """

        album: Album = self.get_object()
        user = self.request.user
        photo_ids = list(set(self.request.data.get('photos')))

        # get photos from the ids that belong to user
        user_photos = Photo.user_objects.queryset(user_id=user.id).filter(id__in=photo_ids)

        for p in user_photos:
            album.photos.remove(p)

        return Response(status=status.HTTP_200_OK)
