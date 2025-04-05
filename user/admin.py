from django.contrib import admin
from . import models
admin.site.register(models.User)
admin.site.register(models.Music)
admin.site.register(models.Album)
admin.site.register(models.Playlist)
# Register your models here.
