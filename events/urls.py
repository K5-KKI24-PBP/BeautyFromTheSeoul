from django.urls import path
from events.views import show_events, create_event, edit_event, \
    show_json, show_json_rsvp, filter_events, user_info, rsvp_ajax, \
    delete_rsvp_ajax, delete_event_ajax, create_event_flutter, delete_event_flutter, edit_event_flutter, \
    get_event, rsvp_flutter, cancel_rsvp_flutter

app_name = 'events'

urlpatterns = [
    path('', show_events, name='event'),
    path('create/', create_event, name='create_event'),
    path('edit/<uuid:id>/', edit_event, name='edit_event'),
    path('event-json/', show_json, name='show_json'),
    path('rsvp-json/', show_json_rsvp, name='show_json_rsvp'),
    path('filter-events/', filter_events, name='filter_events'),
    path('user-info/', user_info, name='user_info'),
    path('rsvp-ajax/<uuid:event_id>/', rsvp_ajax, name='rsvp_ajax'),
    path('cancel-rsvp-ajax/<uuid:event_id>/', delete_rsvp_ajax, name='delete_ajax'),
    path('delete-event-ajax/<uuid:id>/', delete_event_ajax, name='delete_event_ajax'),
    path('create-event-flutter/', create_event_flutter, name='create_event_flutter'),
    path('delete-event-flutter/<uuid:id>/', delete_event_flutter, name='delete_event_flutter'),
    path('edit-event-flutter/<uuid:id>/', edit_event_flutter, name='edit_event_flutter'),
    path('get-event/<uuid:id>/', get_event, name='get_event'),
    path('rsvp-flutter/<uuid:event_id>/', rsvp_flutter, name='rsvp_flutter'),
    path('cancel-rsvp-flutter/<uuid:event_id>/', cancel_rsvp_flutter, name='cancel_rsvp_flutter'),
]