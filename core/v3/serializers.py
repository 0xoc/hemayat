from rest_framework import serializers
from core.models import Location, Note, UserProfile, NoteType


class NoteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteType
        fields = ['pk', 'title']


class UserProfileSerializer(serializers.ModelSerializer):
    """
        UserProfile Retrieve serializer
    """

    username = serializers.CharField(source='user.username')

    class Meta:
        model = UserProfile
        fields = ['username', ]

        ref_name = "UesrProfile.v2"


class NoteSerializer(serializers.ModelSerializer):
    """
        Note CRUD Serializre
    """

    user_profile = UserProfileSerializer(read_only=True)
    # note_type = NoteTypeSerializer()

    class Meta:
        model = Note
        fields = ['pk', 'title', 'text', 'note_type', 'location', 'timestamp', 'user_profile']

        ref_name = "Note.v2"


class LocationSerializer(serializers.ModelSerializer):
    """
        Location CRUD Serializer
    """

    # latest_note = NoteSerializer(read_only=True)
    # note_type = NoteTypeSerializer()

    class Meta:
        model = Location
        fields = ['pk', 'title', 'latitude', 'longitude', 'note_text', 'note_type',
                  'postal_code',
                  'pelak',
                  'sarparast',
                  'mantaqe',
                  'rabet',
                  # 'latest_note'
                  ]

        ref_name = "Location.v2"
