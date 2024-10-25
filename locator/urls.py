from django.urls import path
from locator.views import show_locator, create_location_entry, show_xml, show_json, delete_location, edit_location, filter_locations

app_name = 'locator'

urlpatterns = [
    path('', show_locator, name='locator'),
    path('create/', create_location_entry, name='location_entry'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('delete/<uuid:id>', delete_location, name='delete_location'),
    path('edit-location/<uuid:id>', edit_location, name='edit_location'),
    path('filter-locations/', filter_locations, name='filter_locations'), 
]
