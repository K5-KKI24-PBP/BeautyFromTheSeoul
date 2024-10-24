from django.urls import path
from locator.views import show_locator, create_location_entry, show_xml, show_json

app_name = 'locator'

urlpatterns = [
    path('', show_locator, name='locator'),
    path('create/', create_location_entry, name='location_entry'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
]
