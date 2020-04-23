from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveAPIView,
                                     RetrieveUpdateDestroyAPIView, UpdateAPIView, GenericAPIView)
from rest_framework.mixins import ListModelMixin
from rest_framework.request import clone_request
from rest_framework.response import Response

from core.models import Location, Note, NoteType
from core.v3.serializers import LocationSerializer, NoteSerializer, NoteTypeSerializer
from rest_framework.permissions import IsAuthenticated


class AllowPUTAsCreateMixin(object):
    """
    The following mixin class may be used in order to support PUT-as-create
    behavior for incoming requests.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object_or_none()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if instance is None:
            ### Commented these lines because I dont't get values from url
            # lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            # lookup_value = self.kwargs[lookup_url_kwarg]
            # extra_kwargs = {self.lookup_field: lookup_value}
            # serializer.save(**extra_kwargs)

            serializer.save(created_by=self.request.user.user_profile, updated_by=self.request.user.user_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        serializer.save(updated_by=self.request.user.user_profile)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def get_object_or_none(self):
        try:
            return self.get_object()
        except Http404:
            if self.request.method == 'PUT':
                # For PUT-as-create operation, we need to ensure that we have
                # relevant permissions, as if this was a POST request.  This
                # will either raise a PermissionDenied exception, or simply
                # return None.
                self.check_permissions(clone_request(self.request, 'POST'))
            else:
                # PATCH requests where the object does not exist should still
                # return a 404 response.
                raise


class MultipleFieldLookupMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """

    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.get_serializer_context()['request'].data[field]:  # Ignore empty fields.
                filter[field] = self.get_serializer_context()['request'].data[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


class SetLocationNoteView(AllowPUTAsCreateMixin, MultipleFieldLookupMixin, UpdateAPIView):
    """
        Create Location

        create location view
    """

    lookup_fields = ['latitude', 'longitude']
    queryset = Location.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = LocationSerializer


class CreateLocationView(CreateAPIView):
    """
        Create Location
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = LocationSerializer


class ListLocationsView(ListAPIView):
    """
        List Locations view

        list of all locations
    """
    permission_classes = (IsAuthenticated,)

    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LocaitionRUDView(RetrieveUpdateDestroyAPIView):
    """
        Retrieve Update Destroy Locaition View

        retrieve update destroy a location by id        
    """
    permission_classes = (IsAuthenticated,)

    serializer_class = LocationSerializer
    queryset = Location.objects.all()

    lookup_url_kwarg = 'location_id'


class NoteTypesListView(ListAPIView):
    """
        Retrieve Update Destroy Locaition View

        retrieve update destroy a location by id
    """
    permission_classes = (IsAuthenticated,)

    serializer_class = NoteTypeSerializer
    queryset = NoteType.objects.all()


class LocationNotesListView(ListModelMixin, GenericAPIView):
    """
        List Location Notes

        list of notes of a given location
    """
    permission_classes = (IsAuthenticated,)

    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(
            location__latitude=self.get_serializer_context()['request'].data['latitude'],
            location__longitude=self.get_serializer_context()['request'].data['longitude']
        ).order_by('-id')

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CreateNoteView(CreateAPIView, ):
    """
        Create Note

        create note for on a location
    """
    permission_classes = (IsAuthenticated,)

    serializer_class = NoteSerializer

    def perform_create(self, serializer_class):
        serializer_class.save(user_profile=self.request.user.user_profile)


class NoteRUDView(RetrieveUpdateDestroyAPIView):
    """
        Note Retrieve Update Destroy view

        create update destroy a note
    """
    permission_classes = (IsAuthenticated,)

    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    lookup_url_kwarg = 'note_id'
