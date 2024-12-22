from django.urls import path
from locator.views import show_locator, create_location_entry, show_xml, show_json, delete_location, edit_location, filter_locations, create_location_flutter, edit_location_flutter, fetch_locations, delete_location_flutter

app_name = 'locator'

urlpatterns = [
    path('', show_locator, name='locator'),
    path('create/', create_location_entry, name='location_entry'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('delete/<uuid:id>', delete_location, name='delete_location'),
    path('edit-location/<uuid:id>', edit_location, name='edit_location'),
    path('filter-locations/', filter_locations, name='filter_locations'), 
    path('create_location_flutter/', create_location_flutter, name='create_location_flutter'),
    path('edit_location_flutter/<uuid:id>/', edit_location_flutter, name='edit_flutter'),
    path('fetch_location/', fetch_locations, name='fetch_location'),
    path('delete_location/<uuid:id>/', delete_location_flutter, name='delete_location_flutter'),
]
