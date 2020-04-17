from rest_framework import serializers
from core.models import Location, Note, UserProfile


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

    user_profile= UserProfileSerializer(read_only=True)

    class Meta:
        model = Note
        fields = ['pk', 'title', 'text', 'location', 'timestamp', 'user_profile']

        ref_name = "Note.v2"


class LocationSerializer(serializers.ModelSerializer):

    """
        Location CRUD Serializer
    """
    
    latest_note = NoteSerializer(read_only=True)

    class Meta:
        model = Location
        fields = ['pk', 'title', 'latitude', 'longitude',
            'postal_code',
            'pelak',
            'sarparast',
            'mantaqe',
            'rabet',
            'latest_note'
        ]

        ref_name = "Location.v2"

