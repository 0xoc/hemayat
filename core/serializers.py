from rest_framework import serializers
from .models import Location, Note


class LocationSerializer(serializers.ModelSerializer):

    """
        Location CRUD Serializer
    """

    class Meta:
        model = Location
        fields = ['pk', 'title', 'latitude', 'longitude', 'note_text']

        ref_name = "Location.v1"



class NoteSerializer(serializers.ModelSerializer):

    """
        Note CRUD Serializre
    """

    class Meta:
        model = Note
        fields = ['pk', 'title', 'text', 'location', 'timestamp']

        ref_name = "Note.v1"
