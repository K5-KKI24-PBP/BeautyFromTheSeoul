from django.urls import path
from events.views import show_events, create_event, edit_event, delete_event

app_name = 'events'

urlpatterns = [
    path('', show_events, name='event'),
    path('create/', create_event, name='create_event'),
    path('edit/<uuid:id>/', edit_event, name='edit_event'),
    path('delete/<uuid:id>/', delete_event, name='delete_event'),
]