from django.shortcuts import get_object_or_404
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveAPIView,
                                     RetrieveUpdateDestroyAPIView)

from .models import Location, Note
from .serializers import LocationSerializer, NoteSerializer
from rest_framework.permissions import IsAuthenticated


class CreateLocationView(CreateAPIView):
    """
        Create Location

        create location view
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = LocationSerializer


class ListLocationsView(ListAPIView):
    """
        List Locations view

        list of all locations
    """
    permission_classes = (IsAuthenticated, )
    
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LocaitionRUDView(RetrieveUpdateDestroyAPIView):
    """
        Retrieve Update Destroy Locaition View

        retrieve update destroy a location by id        
    """
    permission_classes = (IsAuthenticated, )

    serializer_class = LocationSerializer
    queryset = Location.objects.all()

    lookup_url_kwarg = 'location_id'


class LocationNotesListView(ListAPIView):
    """
        List Location Notes

        list of notes of a given location
    """
    permission_classes = (IsAuthenticated, )

    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(location__pk=self.kwargs.get('location_id')).order_by('-id')



class CreateNoteView(CreateAPIView):
    """
        Create Note

        create note for on a location
    """
    permission_classes = (IsAuthenticated, )

    serializer_class = NoteSerializer


class NoteRUDView(RetrieveUpdateDestroyAPIView):
    """
        Note Retrieve Update Destroy view

        create update destroy a note
    """
    permission_classes = (IsAuthenticated, )

    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    lookup_url_kwarg = 'note_id'
