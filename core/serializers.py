from rest_framework import serializers
from .models import Location, Note


class LocationSerializer(serializers.ModelSerializer):

    """
        Location CRUD Serializer
    """

    class Meta:
        model = Location
        fields = ['pk', 'title', 'latitude', 'longitude', 'note_text']



class NoteSerializer(serializers.ModelSerializer):

    """
        Note CRUD Serializre
    """

    class Meta:
        model = Note
        fields = ['pk', 'title', 'text', 'location', 'timestamp']

