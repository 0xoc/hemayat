from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from core.v2.views import (CreateLocationView, CreateNoteView, ListLocationsView,
                           LocaitionRUDView, LocationNotesListView, NoteRUDView, SetLocationNoteView)
from rest_framework.authtoken import views

schema_view = get_schema_view(
   openapi.Info(
      title="Hemayat API",
      default_version='v2',
      contact=openapi.Contact(email="snparvizi75@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('obtain-auth-token/', views.obtain_auth_token),
    path('location/notes/list/', LocationNotesListView.as_view()),
    path('location/set-note/', SetLocationNoteView.as_view()),
    # location

    path('location/create/', CreateLocationView.as_view()),
    path('location/list/', ListLocationsView.as_view()),
    path('location/<int:location_id>/', LocaitionRUDView.as_view()),
    
    # note
    path('note/create/', CreateNoteView.as_view()),
    path('note/<int:note_id>/', NoteRUDView.as_view()),

    # docs
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]
