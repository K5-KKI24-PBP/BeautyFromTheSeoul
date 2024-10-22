from django.urls import path
from events.views import show_events, create_event

app_name = 'events'

urlpatterns = [
    path('', show_events, name='event'),
    path('create/', create_event, name='create_event'),
]