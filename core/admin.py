from django.contrib import admin
from .models import Note, Location


class LocationAdmin(admin.ModelAdmin):

    list_display = ['pk', 'name', 'lat', 'lon']
    list_editable = ['name', 'lat', 'lon']
    list_display_links = ['pk', ]


class NoteAadmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'lat', 'lon']

    list_display = ['pk', 'title', 'text', 'location', 'timestamp']
    list_display_links = ['pk', ]


admin.site.register(Note, NoteAadmin)
admin.site.register(Location, LocationAdmin)
