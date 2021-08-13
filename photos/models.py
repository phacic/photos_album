from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import File
from django.db import models
from rest_framework.exceptions import ValidationError
from sorl.thumbnail import ImageField

User = get_user_model()


class UserPhotoAlbumManager(models.Manager):
    """ manager to filter photos and albums by user """
    def queryset(self, user_id):
        return self.filter(user_id=user_id)


class Photo(models.Model):

    def validate_image_size(f: File):  # noqa
        """ validate uploaded image size is within range """
        filesize = f.size
        size_limit = int(settings.MAX_IMAGE_SIZE) * 1024 * 1024
        if filesize > size_limit:
            raise ValidationError(f"Max file size is {settings.MAX_IMAGE_SIZE}MB")

    # photo title
    title = models.CharField(max_length=255)
    # user who created the image
    user = models.ForeignKey(User, related_name='photos', on_delete=models.CASCADE)
    # the image itself
    image = ImageField(upload_to='images/photos/%Y/%m/%d', validators=[validate_image_size])
    # created and updated times
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    # manager
    objects = models.Manager()
    user_objects = UserPhotoAlbumManager()

    def __str__(self):
        return f'{self.title}'


class Album(models.Model):
    # album title
    title = models.CharField(max_length=255)
    # user who created the album
    user = models.ForeignKey(User, related_name='albums', on_delete=models.CASCADE)
    # photos associated with the album
    photos = models.ManyToManyField(Photo, related_name='albums', blank=True)
    # created and updated times
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    # manager
    objects = models.Manager()
    user_objects = UserPhotoAlbumManager()

    def __str__(self):
        return f'{self.title}'
