from django.contrib import admin
from .models import Note, Location


class LocationAdmin(admin.ModelAdmin):

    list_display = ['pk', 'title', 'latitude', 'longitude', 'note_text']
    list_editable = ['title', 'note_text']
    list_display_links = ['pk', ]


class NoteAadmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'latitude', 'longitude']

    list_display = ['pk', 'title', 'text', 'location', 'timestamp']
    list_display_links = ['pk', ]


admin.site.register(Note, NoteAadmin)
admin.site.register(Location, LocationAdmin)
