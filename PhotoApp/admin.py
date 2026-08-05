from django.contrib import admin
from .models import Photo

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')

admin.site.register(Photo, PhotoAdmin)