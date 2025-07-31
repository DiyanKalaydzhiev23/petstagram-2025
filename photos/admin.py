from django.contrib import admin

from photos.models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_tagged_pets', 'date_of_publication', 'description']

    @staticmethod
    def get_tagged_pets(obj: Photo):
        return ', '.join(p.name for p in obj.tagged_pets.all())