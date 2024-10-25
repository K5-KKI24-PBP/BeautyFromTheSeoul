from django.urls import path
from events.views import show_events, create_event, edit_event, delete_event, rsvp_event, show_json, show_json_rsvp, delete_rsvp, filter_events

app_name = 'events'

urlpatterns = [
    path('', show_events, name='event'),
    path('create/', create_event, name='create_event'),
    path('edit/<uuid:id>/', edit_event, name='edit_event'),
    path('delete/<uuid:id>/', delete_event, name='delete_event'),
    path('rsvp/<uuid:event_id>/', rsvp_event, name='rsvp_event'),
    path('delete-rsvp/<uuid:event_id>/', delete_rsvp, name='delete_rsvp'),
    path('event-json/', show_json, name='show_json'),
    path('rsvp-json/', show_json_rsvp, name='show_json_rsvp'),
    path('filter-events/', filter_events, name='filter_events')
]