from django.contrib import admin
from django.contrib.auth.models import AbstractUser


from .models import Photo, Album


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner')
    search_fields = ['title', 'owner']

    def owner(self, album: Album):
        return album.user.get_full_name()


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner')
    search_fields = ['title']

    def owner(self, album: Photo):
        return album.user.get_full_name()


# registration
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album, AlbumAdmin)


